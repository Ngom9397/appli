from flask import Flask, render_template, url_for, request, flash, redirect
import psycopg2 as psy

app = Flask(__name__)
app.secret_key = "message"


def connexiondb():
    try:
        connexion = psy.connect(host="localhost",
                                database="flaskapp",
                                user="postgres",
                                password="@Lamine"
                                )
        return connexion
    except (Exception) as error:
        print("Problème de connexion au serveur Postgres", error)


con = connexiondb()
cur = con.cursor()


@app.route('/')
def home():
    return render_template('index.html')

# Menu Scolarite
@app.route('/ajout_app')
def ajout_app():
    con = connexiondb()
    cur = con.cursor()
    cur.execute("SELECT nom,prenom,date_naiss,email,telephone,adresse,nom_promo FROM apprenant,promo WHERE apprenant.id_promo=promo.id_promo")
    data = cur.fetchall()

    cur.execute("SELECT * FROM promo")
    data1 = cur.fetchall()

    return render_template('inscription.html', app=data, pro=data1)


@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if request.method == 'POST':
        # Insertion donnees dans la base

        flash('Apprenant ajouté avec succès!! Merci')

        nom = request.form["nom"]
        prenom = request.form["prenom"]
        date_naiss = request.form["date_naiss"]
        email = request.form["email"]
        telephone = request.form["telephone"]
        adresse = request.form["adresse"]
        promo = request.form["promo"]
        data = (nom, prenom, date_naiss, email, telephone, adresse, promo)
        con = connexiondb()
        cur = con.cursor()
        cur.execute(
            "INSERT INTO apprenant (nom, prenom, date_naiss, email, telephone, adresse,id_promo) VALUES (%s, %s, %s, %s, %s, %s, %s)", (data))

        con.commit()
        cur.close()

        return redirect(url_for('ajout_app'))


@app.route('/ajout_ref',  methods=['GET', 'POST'])
def ajout_ref():
	con = connexiondb()
	cur = con.cursor()
	cur.execute("SELECT * from referentiel")
	data = cur.fetchall()
	con.commit()

	
	if request.method == "POST":
		nom = request.form["nom_ref"]
		cur.execute("INSERT INTO referentiel (nom_ref) VALUES (%s)", (nom,))
		con.commit()
		
		cur.execute("SELECT * from referentiel")
		data1 = cur.fetchall()
		con.commit()

		flash('Nouveau référentiel ajouté  avec succès!!')
		return redirect(url_for('ajout_ref', ref = data1))

		

	return render_template('ajout_ref.html', ref = data)


@app.route('/ajout_promo', methods = ['GET', 'POST'])
def ajout_promo():
	con = connexiondb()
	cur = con.cursor()
	cur.execute("SELECT  nom_promo, date_debut, date_fin, nom_ref FROM promo, referentiel WHERE promo.id_ref=referentiel.id_ref")
	data = cur.fetchall()
	con.commit()

	cur.execute("SELECT * FROM referentiel ")
	data2 = cur.fetchall()
    
	if request.method == "POST":
		nom = request.form["nom_promo"]
		date_debut= request.form["date_debut"]
		date_fin = request.form["date_fin"]
		id_ref = request.form["ref"]
		
		cur.execute("INSERT INTO promo (nom_promo, date_debut, date_fin, id_ref) VALUES (%s, %s, %s, %s)", (nom, date_debut, date_fin, id_ref))
		con.commit()

		cur.execute("SELECT id_promo, nom_promo, date_debut, date_fin FROM promo")
		data1 = cur.fetchall()
		con.commit()

		flash('Promo ajoutée avec succès!! Merci')
		
		return redirect(url_for('ajout_promo', promo = data1, listRef = data2))
		
	return render_template('ajout_promo.html', promo=data, listRef=data2)


@app.route('/modifier', methods=['GET', 'POST'])
def modifier():
	cur.execute("SELECT id_app,nom,prenom,date_naiss,email,telephone,adresse,nom_promo FROM apprenant,promo WHERE apprenant.id_promo=promo.id_promo")
	data=cur.fetchall()
	con.commit()

	cur.execute("select * from promo")
	data1=cur.fetchall()
	con.commit()

	if request.method == "POST":
		id_app = request.form["id_app"]
		nom = request.form["nom"]
		prenom = request.form["prenom"]
		date_naiss = request.form["date_naiss"]
		email = request.form["email"]
		telephone = request.form["telephone"]
		adresse = request.form["adresse"]
		promo = request.form["id_promo"]
		cur.execute("""
		UPDATE apprenant
		SET nom=%s, prenom=%s, date_naiss=%s, email=%s, telephone=%s,
		adresse=%s, id_promo=%s WHERE id_app=%s

		""", (nom, prenom, date_naiss, email, telephone, adresse, promo,id_app))

		con.commit()


		cur.execute("SELECT id_app,nom,prenom,date_naiss,email,telephone,adresse,nom_promo FROM apprenant,promo WHERE apprenant.id_promo=promo.id_promo")
		data2=cur.fetchall()
		con.commit()



		flash('Mise à jour effectuée avec succès!!')

		return render_template('modif.html', app = data2, promo = data1)
	return render_template('modif.html', app = data, promo = data1)


@app.route('/modifier_ref')
def modifier_ref():

	cur.execute("SELECT * FROM referentiel")
	data=cur.fetchall()
	con.commit()
	return render_template('modif_ref.html', ref=data )


@app.route('/modif_ref', methods=['GET', 'POST'])
def modif_ref():
	
	id_re = request.form["id"]
	nom = request.form["nom_ref"]
	cur.execute("""UPDATE referentiel SET nom_ref=%s WHERE id_ref=%s""", (nom, id_re))
	con.commit()

	flash('Modification effectuée avec succès!!')

	# return render_template('modif_ref.html', ref=data1,)
	return redirect(url_for('modifier_ref'))


@app.route('/modif_promo', methods = ['GET', 'POST'])
def modif_promo():
	con = connexiondb()
	cur = con.cursor()
	cur.execute("SELECT  id_promo, nom_promo, date_debut, date_fin, nom_ref FROM promo, referentiel WHERE promo.id_ref=referentiel.id_ref")
	data = cur.fetchall()
	con.commit()

	cur.execute("SELECT * FROM referentiel ")
	data1 = cur.fetchall()
	if request.method == 'POST':
		id_pro = request.form['id_promo']
		nom = request.form["nom_promo"]
		date_debut= request.form["date_debut"]
		date_fin = request.form["date_fin"]
		id_ref = request.form["id_ref"]

		cur.execute("""
		UPDATE promo
		SET nom_promo=%s, date_debut=%s, date_fin=%s, id_ref=%s WHERE id_promo=%s

		""", (nom, date_debut, date_fin, id_ref, id_pro))

		con.commit()


		cur.execute("SELECT  id_promo, nom_promo, date_debut, date_fin, nom_ref FROM promo, referentiel WHERE promo.id_ref=referentiel.id_ref")
		data2=cur.fetchall()
		con.commit()



		flash('Mise à jour effectuée avec succès!!')




		return redirect(url_for("modif_promo", promo = data2, listref = data1))
	return render_template('modif_promo.html',promo = data, listref = data1)



# @app.route('/Scolarité/annuler')
# def annuler():
# 	return render_template('pages/annulation.html')

# @app.route('/Scolarité/suspendre')
# def suspendre():
# 	return render_template('pages/suspension.html')



if __name__ == "__main__":

    app.run(debug=True, port=3000)
