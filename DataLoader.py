"""ESTE ARCHIVO MANEJARA LA CARGA DE INFORMACION Y HARA FUNCIONES BASICAS
   DE Procesado 
"""
import pandas as pd
from inline_sql import sql, sql_val

#normaliza los nombres de las columnas a minuscula por comodidad
def leer_csv(nombre):
    
    if nombre[-4:]!=".csv":
        nombre=nombre+".csv"
    data=pd.read_csv(nombre)
    atributos=data.columns
    columnas=[]
    for atributo in atributos:
        columnas.append(atributo.lower())
    data.columns=columnas
    return data

"""Funcion para corregir la calidad del archivo stores_clusters"""
def importar_cluster_stores():
    from pathlib import Path
    archivo=Path("store_clusters_sin_nulls.csv")
    if not archivo.exists():
        stores=leer_csv("eci_stores")
        clusters_stores=leer_csv("eci_stores_clusters")
        from opencage.geocoder import OpenCageGeocode

        clave = '86efa54a2ee6456e9b1b1c470156275c'
        geocoder = OpenCageGeocode(clave)
        lats=[]
        lngs=[]
        for index, row in stores.iterrows():
            direccion=str(row.iloc[3])+" ,"+str(row.iloc[4])+" ,"+str(row.iloc[5])+" ,"+str(row.iloc[6])+" " +str(row.iloc[7])
            resultados = geocoder.geocode(direccion)
            if resultados:
                lat = resultados[0]['geometry']['lat']
                lng = resultados[0]['geometry']['lng']
                lats.append(lat)
                lngs.append(lng)
            else:
                lats.append(None)
                lngs.append(None)

        stores["lat"]=lats
        stores["lng"]=lngs
        clusters_coordenadas=sql^"""Select s.store_id, s.lat,s.lng, sc.cluster FROM clusters_stores as sc
                   INNER JOIN stores as s on s.store_id=sc.store_id """

        nulls=sql^"""SELECT * FROM clusters_coordenadas WHERE cluster is null"""
        nulls=nulls.sort_values(by="lat")
        etiquetas=["FL_Cluster","GA_Cluster","SC_Cluster","SC_Cluster","SC_Cluster","NC_Cluster","NC_Cluster","NC_Cluster","Textas_Cluster",
        "Midwest_Cluster","Midwest_Cluster","Ohio_Great_Lakes","Ohio_Great_Lakes","NJ_Cluster","Northeast_Cluster","Midwest_Cluster","Northeast_Cluster" ]
        nulls["cluster"]=etiquetas
        for _, row in nulls.iterrows():
            clusters_stores.loc[(clusters_stores["store_id"]==row.iloc[0]),["cluster"]]=row.iloc[3]
        clusters_stores.to_csv("store_clusters_sin_nulls.csv",index=False)
    else:
        return leer_csv("store_clusters_sin_nulls.csv")



"""Funcion_auxiliar para generar un dict[store_id]:cluster
   consejo:
   puede utilizarse para añadir la columna cluster a las_transacciones
   ventas=leer_csv("eci_transacciones") 
   dict=store_cluster() #Tambien se puede usar store_cluster_codigo()
   ventas["cluster"]=ventas["store_id"].map(dict)
"""
def store_cluster():
    store_to_cluster={}
    cluster_csv=importar_cluster_stores()
    for i in range(len(cluster_csv)):
        fila=cluster_csv.iloc[i]
        store_to_cluster[fila.iloc[0]]=fila.iloc[3]
    return store_to_cluster
"""Funcion_auxiliar para generar un dict[cluster]:int
"""
def store_cluster_codigo():
    store_to_cluster=store_cluster() #dict[store_id]:cluster_name
    cluster_csv=leer_csv("Store_clusters_sin_nulls")
    cluster_to_num={} #dict[cluster_name]:int
    clusters=cluster_csv["cluster"].unique()
    
    for i in range(len(clusters)):
        cluster_to_num[clusters[i]]=i

    
    store_to_cluster_num={} #dict[store_id]:int
    for key in store_to_cluster.keys():
        store_to_cluster_num[key]=cluster_to_num[store_to_cluster[key]]
        
    return store_to_cluster_num

"""Funcion para formatear la data ventas remplazando las features categoricas"""
"Genera lag features de la columna 'lag_feature' con retraso igual a 'lag'"
def generar_lag_features(df,lag_feature,lag,categorie="cod_store_subgroup"):
    df[f"{lag_feature}_lag_{lag}"]=df.groupby(categorie)[lag_feature].shift(lag)


def importar_ventas():
	from pathlib import Path
	archivo=Path("ventas_final.csv")
	if not archivo.exists():
		ventas=leer_csv("eci_transactions")
		
		cluster=store_cluster_codigo()
		store_x_subgroup=sql^"""SELECT DISTINCT store_id, subgroup FROM ventas"""

		codigo=range(len(store_x_subgroup)) #productos*tiendas
		store_x_subgroup["cod_store_subgroup"]=codigo
		
		ventas["quantity"]=ventas["total_sales"]//ventas["price"]
		
		ventas=sql^"""SELECT date,store_id,subgroup, sum(quantity) as demand, mean(price) as mean_price FROM ventas GROUP BY date, store_id, subgroup"""
		ventas["cluster"]=ventas["store_id"].map(cluster)
		ventas=ventas.merge(store_x_subgroup,on=["store_id","subgroup"],how="left")
		ventas.drop(["store_id","subgroup"],axis=1,inplace=True)
		ventas=ventas.sort_values(by=["cod_store_subgroup","date"])
		for i in range(1,8): #agregamos lag a 7 dias por que vamos a predecir 7 dias
			generar_lag_features(ventas,"demand",i,"cod_store_subgroup")
		ventas["date"]=pd.to_datetime(ventas["date"])
		ventas["day"]=ventas["date"].dt.day
		ventas["month"]=ventas["date"].dt.month
		ventas["year"]=ventas["date"].dt.year
		ventas.drop("date",axis=1,inplace=True)
		ventas.to_csv("ventas_final.csv",index=False)
		return ventas
	else:
		ventas=leer_csv("ventas_final.csv")
		return ventas



	