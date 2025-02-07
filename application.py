"""
📝 **Instructions** :
- Installez toutes les bibliothèques nécessaires en fonction des imports présents dans le code, utilisez la commande suivante :conda create -n projet python pandas numpy ..........
- Complétez les sections en écrivant votre code où c’est indiqué.
- Ajoutez des commentaires clairs pour expliquer vos choix.
- Utilisez des emoji avec windows + ;
- Interprétez les résultats de vos visualisations (quelques phrases).
"""

### 1. Importation des librairies et chargement des données
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px

# Remplacez "chemin_du_fichier/ds_salaries.csv" par le chemin réel de votre fichier CSV
df = pd.read_csv(r"projet_notebook2/archive/ds_salaries.csv")


### 2. Exploration visuelle des données
#votre code 
st.title("📊 Visualisation des Salaires en Data Science")
st.markdown("Explorez les tendances des salaires à travers différentes visualisations interactives.")


# Création d'une case à cocher pour afficher l'aperçu des données
if st.checkbox("Afficher un aperçu des données"):
    st.write(df.head())  # Afficher les premières lignes du DataFrame


#Statistique générales avec describe pandas 
 
st.subheader("📌 Statistiques générales")
st.write(df.describe())
     



### 3. Distribution des salaires en France par rôle et niveau d'expérience, uilisant px.box et st.plotly_chart
#votre code 
st.subheader("📈 Distribution des salaires en France")
df_france = df[df["employee_residence"] == "FR"]

# Créer une liste déroulante pour sélectionner le niveau d'expérience
experience_selected = st.selectbox(
    "Sélectionnez un niveau d'expérience :", 
    options=df["experience_level"].unique(),
    index=0  # Sélectionne par défaut le premier élément
)
# Filtrer les données en fonction du niveau d'expérience sélectionné
df_filtered = df_france[df_france["experience_level"] == experience_selected]


fig = px.box(
        df_filtered,
        x="job_title",
        y="salary_in_usd",
        title="Distribution des salaires en France par rôle et niveau d'expérience",
        labels={"job_title": "Rôle", "salary_in_usd": "Salaire (€)"}
    )

    # Afficher le graphique avec Streamlit
st.plotly_chart(fig, use_container_width=True)

### 4. Analyse des tendances de salaires :
#### Salaire moyen par catégorie : en choisisant une des : ['experience_level', 'employment_type', 'job_title', 'company_location'], utilisant px.bar et st.selectbox 
# Liste déroulante pour choisir la catégorie d'analyse

categories = ['experience_level', 'employment_type', 'job_title', 'company_location']
selected_category = st.selectbox(
    "Choisissez une catégorie pour voir le salaire moyen :", 
    categories
)

# Calcul du salaire moyen par catégorie sélectionnée
salary_avg = df.groupby(selected_category)["salary"].mean().reset_index()

# Création du graphique en barres
fig = px.bar(
    salary_avg,
    x=selected_category,
    y="salary",
    color=selected_category,  # Ajoute une couleur différente par catégorie
    title=f"Salaire moyen par {selected_category}",
    labels={selected_category: selected_category.capitalize(), "salary": "Salaire moyen (€)"},
)

# Affichage du graphique
st.plotly_chart(fig, use_container_width=True)




### 5. Corrélation entre variables
# Sélectionner uniquement les colonnes numériques pour la corrélation
#votre code 

st.subheader("🔗 Corrélations entre variables numériques")

df_numeric = df.select_dtypes(include=["number"])

# Calcul de la matrice de corrélation
corr_matrix = df_numeric.corr()

# Création d'une figure matplotlib pour afficher la heatmap
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax)

# Affichage du graphique dans Streamlit
st.pyplot(fig)


st.subheader("🔗 Corrélations entre variables numériques")




### 6. Analyse interactive des variations de salaire
# Une évolution des salaires pour les 10 postes les plus courants
# count of job titles pour selectionner les postes
# calcule du salaire moyen par an
#utilisez px.line
#votre code 


# Sélectionner les 10 postes les plus courants
top_jobs = df["job_title"].value_counts().nlargest(10).index.tolist()

# Liste déroulante pour sélectionner un poste parmi les 10 plus courants
selected_job = st.selectbox("Sélectionnez un poste :", top_jobs)

# Filtrer les données pour le poste sélectionné
df_filtered = df[df["job_title"] == selected_job]

# Calcul du salaire moyen par année
salary_trend = df_filtered.groupby("work_year")["salary_in_usd"].mean().reset_index()

# Création du graphique d'évolution des salaires
fig = px.line(
    salary_trend,
    x="work_year",
    y="salary_in_usd",
    markers=True,  # Ajouter des points sur la courbe
    title=f"Évolution du salaire moyen pour {selected_job}",
    labels={"work_year": "Année", "salary_in_usd": "Salaire moyen (€)"},
    line_shape="linear"
)

# Affichage du graphique avec Streamlit
st.plotly_chart(fig, use_container_width=True)




### 7. Salaire médian par expérience et taille d'entreprise
# utilisez median(), px.bar
#votre code 

st.subheader("📊 Salaire médian par expérience et taille d'entreprise")

# Vérifier si les colonnes nécessaires existent

# Calcul du salaire médian par expérience et taille d'entreprise
salary_median = df.groupby(["experience_level", "company_size"])["salary"].median().reset_index()

# Création du graphique en barres
fig = px.bar(
    salary_median,
    x="experience_level",
    y="salary",
    color="company_size",
    barmode="group",  # Afficher les barres côte à côte
    title="Salaire médian par niveau d'expérience et taille d'entreprise",
    labels={"experience_level": "Niveau d'expérience", "salary": "Salaire médian (€)", "company_size": "Taille d'entreprise"},
)

# Affichage du graphique avec Streamlit
st.plotly_chart(fig, use_container_width=True)

### 8. Ajout de filtres dynamiques
#Filtrer les données par salaire utilisant st.slider pour selectionner les plages 
#votre code 


# Sous-titre
st.subheader("🎚️ Filtrage dynamique des salaires")


# Définir les valeurs min et max du salaire
min_salary, max_salary = int(df["salary"].min()), int(df["salary"].max())

# Curseur pour sélectionner une plage de salaires
salary_range = st.slider(
    "Sélectionnez une plage de salaires (€) :",
    min_value=min_salary,
    max_value=max_salary,
    value=(min_salary, max_salary)  # Par défaut, toute la plage est sélectionnée
)

# Filtrer les données en fonction de la plage sélectionnée
df_filtered = df[(df["salary"] >= salary_range[0]) & (df["salary"] <= salary_range[1])]

# Affichage du nombre de lignes après filtrage
st.write(f"📌 Nombre d'enregistrements après filtrage : {df_filtered.shape[0]}")

# Affichage des données filtrées
st.dataframe(df_filtered)


### 9.  Impact du télétravail sur le salaire selon le pays

st.subheader("🏠💼 Impact du télétravail sur le salaire selon le pays")



# Transformer 'remote_ratio' en catégories (Présentiel, Hybride, Télétravail)
df["work_type"] = df["remote_ratio"].apply(lambda x: "Présentiel" if x == 0 else ("Hybride" if x == 50 else "Télétravail"))

# Sélecteur pour choisir un ou plusieurs pays
selected_countries = st.multiselect(
    "🌍 Sélectionnez un ou plusieurs pays :",
    df["company_location"].unique(),
    default=df["company_location"].unique()[:5]  # Sélectionne les 5 premiers par défaut
)

# Filtrer les données en fonction des pays sélectionnés
df_filtered = df[df["company_location"].isin(selected_countries)]

# Calcul du salaire moyen par pays et mode de travail
salary_by_remote = df_filtered.groupby(["company_location", "work_type"])["salary"].mean().reset_index()

# Création du graphique en barres
fig = px.bar(
    salary_by_remote,
    x="company_location",
    y="salary",
    color="work_type",
    barmode="group",
    title="📊 Salaire moyen par mode de travail et pays",
    labels={"company_location": "Pays", "salary": "Salaire moyen (€)", "work_type": "Mode de travail"}
)

# Affichage du graphique
st.plotly_chart(fig, use_container_width=True)

# Affichage des données sous forme de tableau
st.dataframe(salary_by_remote)


### 10. Filtrage avancé des données avec deux st.multiselect, un qui indique "Sélectionnez le niveau d'expérience" et l'autre "Sélectionnez la taille d'entreprise"
#votre code 

# Sous-titre
st.subheader("🔎 Filtrage avancé des données")


# Sélecteur pour le niveau d'expérience
experience_selected = st.multiselect(
    "📌 Sélectionnez le niveau d'expérience :",
    df["experience_level"].unique(),
    default=df["experience_level"].unique()  # Tout sélectionner par défaut
)

# Sélecteur pour la taille d'entreprise
company_size_selected = st.multiselect(
    "🏢 Sélectionnez la taille d'entreprise :",
    df["company_size"].unique(),
    default=df["company_size"].unique()  # Tout sélectionner par défaut
)

# Filtrer les données en fonction des choix de l'utilisateur
df_filtered = df[
    (df["experience_level"].isin(experience_selected)) &
    (df["company_size"].isin(company_size_selected))
]

# Affichage du nombre d'enregistrements après filtrage
st.write(f"📌 Nombre d'enregistrements après filtrage : {df_filtered.shape[0]}")

# Affichage des données filtrées sous forme de tableau interactif
st.dataframe(df_filtered)
