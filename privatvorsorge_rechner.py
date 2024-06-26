from datetime import datetime

class colors: # https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal
	CEND      = '\33[0m'
	CBOLD     = '\33[1m'
	CITALIC   = '\33[3m'
	CURL      = '\33[4m'
	CBLINK    = '\33[5m'
	CBLINK2   = '\33[6m'
	CSELECTED = '\33[7m'

	CBLACK  = '\33[30m'
	CRED    = '\33[31m'
	CGREEN  = '\33[32m'
	CYELLOW = '\33[33m'
	CBLUE   = '\33[34m'
	CVIOLET = '\33[35m'
	CBEIGE  = '\33[36m'
	CWHITE  = '\33[37m'

	CBLACKBG  = '\33[40m'
	CREDBG    = '\33[41m'
	CGREENBG  = '\33[42m'
	CYELLOWBG = '\33[43m'
	CBLUEBG   = '\33[44m'
	CVIOLETBG = '\33[45m'
	CBEIGEBG  = '\33[46m'
	CWHITEBG  = '\33[47m'

	CGREY    = '\33[90m'
	CRED2    = '\33[91m'
	CGREEN2  = '\33[92m'
	CYELLOW2 = '\33[93m'
	CBLUE2   = '\33[94m'
	CVIOLET2 = '\33[95m'
	CBEIGE2  = '\33[96m'
	CWHITE2  = '\33[97m'

def funktion_invertieren(funktion, funktionswert, name_zu_bestimmender_parameter, uebrige_parameter, praezision=0.01, initialer_schaetzwert=1):
	param_estimate = initialer_schaetzwert
	step_size = 0.01
	last_estimate_was_overestimate = None
	while True: # Solange der Fehler über der gewünschten Präzision liegt (s.u.):
		params = uebrige_parameter
		params[name_zu_bestimmender_parameter] = param_estimate
		error = funktion(**params) - funktionswert # = estimate - target
		if abs(error) <= praezision:
			break # we're done, our estimate is within the chosen precision of the actual value
		if error > 0: # we're overestimating, our estimate is too big:
			param_estimate -= step_size
			if last_estimate_was_overestimate == False: # last time we underestimated and now we overstimated => our step size is too large
				step_size *= 0.5 # half step size
			last_estimate_was_overestimate = True
		else: # we're underestimating, our estimate is too small:
			param_estimate += step_size
			if last_estimate_was_overestimate == True: # last time we overestimated and now we underestimated => our step size is too large
				step_size *= 0.5 # half step size
			last_estimate_was_overestimate = False
	return param_estimate

print("##### Privatvorsorge-Rechner: #####")

# Nutzer-Abfragen:

aktuelles_jahr = datetime.now().year

geburts_jahr = int(input(">>> In welchem Jahr wurdest du geboren?: "))
aktuelles_alter_in_jahren = aktuelles_jahr - geburts_jahr

renteneintritts_jahr = int(input(">>> In welchem Jahr möchtest du in Rente gehen?: "))
if renteneintritts_jahr <= aktuelles_jahr:
	print(f"Fehler: Das Renteneintritts-Jahr muss in der Zukunft liegen!")
	exit(1)
dauer_sparphase_in_jahren = renteneintritts_jahr - aktuelles_jahr

lebenserwartung = int(input(">>> Welche Lebenserwartung möchtest du für dich/deine Rente ansetzen?: "))
dauer_rentenphase_in_jahren = lebenserwartung - aktuelles_alter_in_jahren - dauer_sparphase_in_jahren
print(f"Du möchtest {dauer_rentenphase_in_jahren} Jahre lang eine Rente beziehen.")

monatliche_wunschrente = float(input(">>> Wie hoch ist deine monatliche Wunschrente? (in Euro): "))
if monatliche_wunschrente <= 0:
	print(f"Fehler: Die monatliche Wunschrente muss eine positive, von Null verschiedene, Zahl sein!")
	exit(1)

inflations_anpassung = input(">>> Meinst du damit die heutige Kaufkraft, d.h. soll diese Wunschrente an die Inflation angepasst werden? (j/N): ")
standardwert_inflation = 2.5
angenommene_inflationsrate_in_prozent = input(f">>> Welche jährliche Inflationsrate soll für sämtliche Berechnungen angenommen werden? (in Prozent, Standardwert: {standardwert_inflation}%): ")
if angenommene_inflationsrate_in_prozent.strip() == "":
	angenommene_inflationsrate_in_prozent = standardwert_inflation
else:
	angenommene_inflationsrate_in_prozent = float(angenommene_inflationsrate_in_prozent)
print(f"Es wird für sämtliche Berechnungen eine jährliche Inflation in Höhe von {angenommene_inflationsrate_in_prozent}% angenommen.")

if inflations_anpassung in ["j", "J"]:
	monatliche_wunschrente = monatliche_wunschrente * ( (1.0 + angenommene_inflationsrate_in_prozent/100.0)**dauer_sparphase_in_jahren )
	print(f"Es wird nun eine inflationsangepasste Wunschrente von {monatliche_wunschrente} Euro/Monat für das Jahr {renteneintritts_jahr} angenommen.")
else:
	print(f"Es wird eine Wunschrente von {monatliche_wunschrente} Euro/Monat für das Jahr {renteneintritts_jahr} angenommen.")

# Berechne und zeige außerdem wie hoch die Rente inflationsangepasst zum Renten-ENDE(!) sein müsste:
noetige_inflationsangepasste_rente_zum_rentenende = monatliche_wunschrente * ( (1.0 + angenommene_inflationsrate_in_prozent/100.0)**dauer_rentenphase_in_jahren ) # Achtung(!): monatliche_wunschrente wurde soeben bereits an die Inflation in der Sparphase angepasst!!!
print(f"{dauer_rentenphase_in_jahren} Jahre später, zum Rentenende mit {lebenserwartung} im Jahre {geburts_jahr+lebenserwartung} müsste die Rente inflationsangepasst {noetige_inflationsangepasste_rente_zum_rentenende} Euro/Monat betragen (im Fall, dass die Rente in der Rentenphase mit der Inflation steigen soll).")

jaehrliche_wunschrente = 12 * monatliche_wunschrente



# ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### #####
# ##### ##### ##### Vermögens-erhaltende Verrentungen: ##### ##### #####
# ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### #####
print("")
print(colors.CRED + "##### ##### ##### Vermögens-erhaltende Verrentungen: ##### ##### #####" + colors.CEND)

# ##### Dividenden-Strategie: #####
print("")
print(colors.CRED + "##### Dividenden-Strategie: #####" + colors.CEND)
angenommene_dividendenrendite_in_prozent = 3.0
notwendiges_vermoegen_in_dividendenaktien = jaehrliche_wunschrente / (angenommene_dividendenrendite_in_prozent / 100.0)
print(f"Unter Annahme einer Dividendenrendite von {angenommene_dividendenrendite_in_prozent}% " +\
	f"musst du im Jahr {renteneintritts_jahr} ein Vermögen in Dividendenaktien/-fonds in Höhe von {notwendiges_vermoegen_in_dividendenaktien} Euro " +\
	f"aufgebaut haben, um deine monatliche Wunschrente in Höhe von {monatliche_wunschrente} Euro in Form von Dividenden zu erhalten.")
notwendige_monatliche_sparrate_fuer_dividenden_strategie_ohne_wertzuwachs_der_aktien = ((jaehrliche_wunschrente/dauer_sparphase_in_jahren)/12) / (angenommene_dividendenrendite_in_prozent / 100.0)

def sparplan_ausfuehren(sparrate_initial, sparrate_steigerungsrate, wertsteigerung_anlageobjekt, anlage_dauer): # (alles in Jahren bzw. pro Jahr)
	vermoegen = 0
	sparrate = sparrate_initial
	for jahr in range(anlage_dauer):
		vermoegen += sparrate
		sparrate *= sparrate_steigerungsrate
		vermoegen *= wertsteigerung_anlageobjekt
	return vermoegen

# Berechnung notwendige konstante monatliche Sparrate für die Dividenstrategie, unter der Annahme, dass das Fondsvermögen mit der Inflation mitwächst:
notwendige_konstante_monatliche_sparrate_fuer_dividenden_strategie_real = (1.0/12.0) * funktion_invertieren(sparplan_ausfuehren, notwendiges_vermoegen_in_dividendenaktien, "sparrate_initial", {"sparrate_steigerungsrate": 1.00, "wertsteigerung_anlageobjekt": 1.00 + (angenommene_inflationsrate_in_prozent/100.0), "anlage_dauer": dauer_sparphase_in_jahren})

# Berechnung notwendige mit der Inflation mitwachsende monatliche Sparrate für die Dividenstrategie, unter der Annahme, dass das Fondsvermögen mit der Inflation mitwächst:
notwendige_wachsende_monatliche_sparrate_fuer_dividenden_strategie_real = (1.0/12.0) * funktion_invertieren(sparplan_ausfuehren, notwendiges_vermoegen_in_dividendenaktien, "sparrate_initial", {"sparrate_steigerungsrate": 1.00 + (angenommene_inflationsrate_in_prozent/100.0), "wertsteigerung_anlageobjekt": 1.00 + (angenommene_inflationsrate_in_prozent/100.0), "anlage_dauer": dauer_sparphase_in_jahren})

print(f"Um innerhalb von {dauer_sparphase_in_jahren} Jahren ein Dividendenportfolio in der Größe von {notwendiges_vermoegen_in_dividendenaktien} Euro " +\
	f"angespart zu haben, müsstest du in der Ansparphase monatlich {notwendige_monatliche_sparrate_fuer_dividenden_strategie_ohne_wertzuwachs_der_aktien} Euro anlegen, " +\
	f"unter der Annahme, dass die Dividendenaktiven/-fonds keinen nominalen Wertzuwachs aufweisen.")
print(f"Da in der Realität jedoch zumindest ein nominaler/inflationsausgleichender " +\
	f"(wenn auch kein realer) Wertzuwachs zu erwarten ist, verringert sich deine notwendige monatliche Sparrate auf {notwendige_konstante_monatliche_sparrate_fuer_dividenden_strategie_real} Euro.")
print(f"Alternativ kannst du auch mit einer monatlichen Sparrate von {notwendige_wachsende_monatliche_sparrate_fuer_dividenden_strategie_real} Euro beginnen und diese jedes Jahr mit der Inflation von {angenommene_inflationsrate_in_prozent}% mitwachsen lassen.")
print("")
print(f"Monatliche Rente in Höhe von {monatliche_wunschrente} Euro ({colors.CRED}brutto{colors.CEND}):")
print(f"=> Hypothetische obere Schranke der monatlichen Sparrate = {notwendige_monatliche_sparrate_fuer_dividenden_strategie_ohne_wertzuwachs_der_aktien} Euro")
print(f"=> Nötige monatliche Sparrate (konstant) = {colors.CRED}{notwendige_konstante_monatliche_sparrate_fuer_dividenden_strategie_real} Euro{colors.CEND}")
print(f"=> Nötige monatliche Sparrate (muss jedes Jahr um {angenommene_inflationsrate_in_prozent}% erhöht werden) = {colors.CRED}{notwendige_wachsende_monatliche_sparrate_fuer_dividenden_strategie_real} Euro{colors.CEND}")
print(f"=> Beachte hierbei, dass mit der Zeit auch dein passives Dividenden-Einkommen steigt. Du kannst dieses natürlich zur Tilgung deiner Sparrate verwenden, also reinvestieren!")
print("")

# Dividenden-Strategie, nun Netto-Betrachtung, also mit Steuern(!):
kapitalertragssteuer_in_prozent = 26.3750 # (in Prozent; vom Gesetzgeber festgelegt)
freibetrag_in_euro = 1000 # (pro Jahr; vom Gesetzgeber festgelegt)
noetige_jaehrliche_bruttorente = 0
if jaehrliche_wunschrente < freibetrag_in_euro: # Die jährliche Wunschrente liegt unter dem Freibetrag...
	noetige_jaehrliche_bruttorente = jaehrliche_wunschrente # ...dann ist Bruttorente == Nettorente.
else:
	# Es soll gelten: freibetrag_in_euro + (noetige_jaehrliche_bruttorente - freibetrag_in_euro) * (1 - 26.3750%) = jaehrliche_wunschrente
	# Umstellen liefert: noetige_jaehrliche_bruttorente = (jaehrliche_wunschrente - freibetrag_in_euro) / (1 - 26.3750%) + freibetrag_in_euro
	noetige_jaehrliche_bruttorente = (jaehrliche_wunschrente - freibetrag_in_euro) / (1 - kapitalertragssteuer_in_prozent/100.0) + freibetrag_in_euro

notwendiges_vermoegen_in_dividendenaktien = noetige_jaehrliche_bruttorente / (angenommene_dividendenrendite_in_prozent / 100.0)

notwendige_monatliche_sparrate_fuer_dividenden_strategie_ohne_wertzuwachs_der_aktien = ((noetige_jaehrliche_bruttorente/dauer_sparphase_in_jahren)/12) / (angenommene_dividendenrendite_in_prozent / 100.0)
notwendige_konstante_monatliche_sparrate_fuer_dividenden_strategie_real = (1.0/12.0) * funktion_invertieren(sparplan_ausfuehren, notwendiges_vermoegen_in_dividendenaktien, "sparrate_initial", {"sparrate_steigerungsrate": 1.00, "wertsteigerung_anlageobjekt": 1.00 + (angenommene_inflationsrate_in_prozent/100.0), "anlage_dauer": dauer_sparphase_in_jahren})
notwendige_wachsende_monatliche_sparrate_fuer_dividenden_strategie_real = (1.0/12.0) * funktion_invertieren(sparplan_ausfuehren, notwendiges_vermoegen_in_dividendenaktien, "sparrate_initial", {"sparrate_steigerungsrate": 1.00 + (angenommene_inflationsrate_in_prozent/100.0), "wertsteigerung_anlageobjekt": 1.00 + (angenommene_inflationsrate_in_prozent/100.0), "anlage_dauer": dauer_sparphase_in_jahren})

print(f"Monatliche Rente in Höhe von {monatliche_wunschrente} Euro ({colors.CRED}netto{colors.CEND}, {kapitalertragssteuer_in_prozent}% Kapitalertragssteuer, {freibetrag_in_euro} Euro Freibetrag):")
print(f"=> Nötige Brutto-Rente zur Erreichung einer Netto-Rente von {monatliche_wunschrente} Euro = {noetige_jaehrliche_bruttorente/12.0} Euro")
print(f"=> Hypothetische obere Schranke der monatlichen Sparrate = {notwendige_monatliche_sparrate_fuer_dividenden_strategie_ohne_wertzuwachs_der_aktien} Euro")
print(f"=> Nötige monatliche Sparrate (konstant) = {colors.CRED}{notwendige_konstante_monatliche_sparrate_fuer_dividenden_strategie_real} Euro{colors.CEND}")
print(f"=> Nötige monatliche Sparrate (muss jedes Jahr um {angenommene_inflationsrate_in_prozent}% erhöht werden) = {colors.CRED}{notwendige_wachsende_monatliche_sparrate_fuer_dividenden_strategie_real} Euro{colors.CEND}")
print(f"=> Beachte hierbei, dass mit der Zeit auch dein passives Dividenden-Einkommen steigt. Du kannst dieses natürlich zur Tilgung deiner Sparrate verwenden, also reinvestieren!")

# Dividenden-Strategie, Vor- und Nachteile:
print("")
print("=> Vor- und Nachteile:")
print(f"(+) Vorteilhaft ist, dass zu erwarten ist, dass sich die Dividenden, also deine Rente, auch in deiner Rentenzeit erhöhen und an die Inflation anpassen werden.")
print(f"(+) Du hast bereits vor Rentenbeginn ein passives Einkommen!")
print(f"(+) Außerdem kannst du deine Dividendenaktien/-fonds problemlos vererben (abzüglich Erbschaftssteuer von 7-30 %, der Freibetrag liegt hier bei 500.000 Euro für Ehegatten und 400.000 Euro für Kinder).")
print(f"(-) Nachteilhaft ist, dass Dividenden Schwankungen unterliegen und in Krisenzeiten auch mal ganz ausfallen können. Eine Diversifizierung der Dividenden-Aktien ist dringend anzuraten!")
print(f"(-) Außerdem ist die Wertsteigerung von Dividenden-Aktien i.d.R. gering, wodurch kein Zinseszinseffekt eintritt und sehr hohe Summen in der Ansparphase angespart werden müssen!")
print(f"(-) Es besteht eine Unsicherheit, wie im Jahr {renteneintritts_jahr} Kapitalerträge versteuert werden.")

# ##### Besparen des MSCI World, regelmäßige Entnahme, unter Erhalt des Vermögens: #####
print("")
print(colors.CRED + "##### Besparen des MSCI World, regelmäßige Entnahme, unter Erhalt des Vermögens (Annahmen: keine Anpassung an die Inflation während der Rentenphase, kein Entnahmeplan): #####" + colors.CEND)
"""
* Laut Finanztip hat der MSCI World in der Vergangenheit eine jährliche Rendite von 9,2% erzielt. (https://www.finanztip.de/indexfonds-etf/msci-world/)
* Das Handelsblatt (vom 21.06.2024) nimmt für den für die Rente besparten ETF eine Rendite von 7,0% (nach Kosten) an.
"""
msci_world_rendite = 7.0
msci_world_monatliche_rendite = 100.0 * ((1.0 + msci_world_rendite/100.0)**(1.0/12.0) - 1.0) # = 0,5654145387% bei 7,0% p.a. # = etwas weniger als msci_world_rendite / 12.0  # (Da wir versuchen, konservativ zu sein, nehmen wir natürlich die geringere Rendite, die außerdem mathematisch korrekter ist!)
print(f"Nehmen wir nun an, dass du mit deinen monatlichen Sparbeiträgen einen ETF auf den MSCI World (oder einen vergleichbaren Fond) besparst (Sparplan).")
print(f"Nehmen wir ferner an, dass der MSCI World eine jährliche Rendite von {msci_world_rendite}% abwirft.")
print(f"Schließlich nehmen wir an, dass du in deiner Rentenphase jeden Monat deine Rente in Höhe von {monatliche_wunschrente} Euro (brutto/netto je nach Betrachtung, s.u.) durch den Verkauf von Anteilen entnimmst " +\
	f"und dass du außerdem möchtest, dass sich dein im ETF befindliches Vermögen nicht verringert, sondern konstant bleibt, dass deine Entnahmen also " +\
	f"durch die jährliche Wertsteigerung des MSCI World um {msci_world_rendite}% wieder \"genau\" ausgeglichen werden.")
print(f"Wir nehmen außerdem an, dass kein Inflationsausgleich in der Rentenphase stattfinden soll, dass die in der Rentenphase entnommene monatliche Rente also konstant bleibt.")
print(f"Ferner gehen wir davon aus, dass du keinen separaten Entnahmeplan durchführst, die Rente also direkt durch regelmäßige Verkäufe deiner ETF-Anteile realisierst.")

# Für die monatliche Wunschrente von {monatliche_wunschrente} Euro, wie hoch muss mein Vermögen im MSCI World sein, damit
#   das jährliche Wachstum des MSCI World von {msci_world_rendite} Prozent meine monatlichen Entnahmen in Höhe von {monatliche_wunschrente} Euro
#   stets exakt ausgleicht?
# => Die monatliche Entnahme {monatliche_wunschrente} muss exakt {notwendiges_vermoegen_im_msci * msci_world_monatliche_rendite} betragen!
# => Umgestellt heißt das: notwendiges_vermoegen_im_msci = monatliche_wunschrente / msci_world_monatliche_rendite
notwendiges_vermoegen_im_msci = monatliche_wunschrente / ( msci_world_monatliche_rendite/100.0 ) # = 17.686,1387805697 EUR bei einer monatlichen Wunschrente von 100EUR und msci_world_rendite = 7.0  # = 17.142,8571428571 EUR bei stupider Rechnung von 100/(7%/12), was allerdings eine leicht zu hohe monatliche Rendite annehmen würde!!!

# Berechnung notwendige konstante monatliche Sparrate für die MSCI-World-Vermögenserhaltende-Monatliche-Entnahme-Strategie, unter der Annahme, dass das Fondsvermögen jährlich um msci_world_rendite% wächst:
notwendige_konstante_monatliche_sparrate_fuer_msci_erhaltende_monatliche_entnahme_strategie = (1.0/12.0) * funktion_invertieren(sparplan_ausfuehren, notwendiges_vermoegen_im_msci, "sparrate_initial", {"sparrate_steigerungsrate": 1.00, "wertsteigerung_anlageobjekt": 1.00 + (msci_world_rendite/100.0), "anlage_dauer": dauer_sparphase_in_jahren})

# Berechnung notwendige mit der Inflation mitwachsende monatliche Sparrate für die MSCI-World-Vermögenserhaltende-Monatliche-Entnahme-Strategie, unter der Annahme, dass das Fondsvermögen jährlich um msci_world_rendite% wächst:
notwendige_wachsende_monatliche_sparrate_fuer_msci_erhaltende_monatliche_entnahme_strategie = (1.0/12.0) * funktion_invertieren(sparplan_ausfuehren, notwendiges_vermoegen_im_msci, "sparrate_initial", {"sparrate_steigerungsrate": 1.00 + (angenommene_inflationsrate_in_prozent/100.0), "wertsteigerung_anlageobjekt": 1.00 + (msci_world_rendite/100.0), "anlage_dauer": dauer_sparphase_in_jahren})

print(f"In diesem Fall muss dein monatlicher Sparbetrag konstant {notwendige_konstante_monatliche_sparrate_fuer_msci_erhaltende_monatliche_entnahme_strategie} Euro betragen, wenn du eine monatliche Rente in Höhe von {monatliche_wunschrente} Euro (brutto) entnehmen können möchtest.")
print(f"Lässt du deinen monatlichen Sparbetrag mit der Inflation jedes Jahr um {angenommene_inflationsrate_in_prozent}% wachsen, so genügt zu Beginn auch ein monatlicher Sparbetrag von nur {notwendige_wachsende_monatliche_sparrate_fuer_msci_erhaltende_monatliche_entnahme_strategie} Euro. Auch dann erreichst du deine monatliche Wunschrente von {monatliche_wunschrente} Euro (brutto), ohne Vermögensverlust.")
print(f"In beiden Fällen wird dein im MSCI World angespartes Vermögen zum Renteneintritt (im Jahre {renteneintritts_jahr}) {notwendiges_vermoegen_im_msci} Euro betragen.")
print(f"Soll deine Rente hingegen {monatliche_wunschrente} Euro (netto) betragen, so ist dies abhängig davon, wie Kapitalerträge im Jahr {renteneintritts_jahr} (und darüber hinaus) besteuert werden, wir betrachten hierzu 3 Szenarien: (1) Kapitalertragssteuer, (2) Einkommensteuer, ledig, (3) Einkommensteuer, verheiratet:")
print("")
print(f"(0) Monatliche Rente in Höhe von {monatliche_wunschrente} Euro ({colors.CRED}brutto{colors.CEND}):")
print(f"=> Nötige monatliche Sparrate (konstant) = {colors.CRED}{notwendige_konstante_monatliche_sparrate_fuer_msci_erhaltende_monatliche_entnahme_strategie} Euro{colors.CEND}")
print(f"=> Nötige monatliche Sparrate (muss jedes Jahr um {angenommene_inflationsrate_in_prozent}% erhöht werden) = {colors.CRED}{notwendige_wachsende_monatliche_sparrate_fuer_msci_erhaltende_monatliche_entnahme_strategie} Euro{colors.CEND}")
print("")
print(f"(1) Monatliche Rente in Höhe von {monatliche_wunschrente} Euro ({colors.CRED}netto{colors.CEND}, {kapitalertragssteuer_in_prozent}% Kapitalertragssteuer, {freibetrag_in_euro} Euro Freibetrag):")
print(f"=> Nötige monatliche Sparrate (konstant) = {colors.CRED}{0} Euro{colors.CEND}") # !!!ToDo!!!
print(f"=> Nötige monatliche Sparrate (muss jedes Jahr um {angenommene_inflationsrate_in_prozent}% erhöht werden) = {colors.CRED}{0} Euro{colors.CEND}") # !!!ToDo!!!
print("")
print(f"(2) Monatliche Rente in Höhe von {monatliche_wunschrente} Euro ({colors.CRED}netto{colors.CEND}, progressiver persönlicher Einkommensteuersatz, ledig):")
print(f"=> Nötige monatliche Sparrate (konstant) = {colors.CRED}{0} Euro{colors.CEND}") # !!!ToDo!!!
print(f"=> Nötige monatliche Sparrate (muss jedes Jahr um {angenommene_inflationsrate_in_prozent}% erhöht werden) = {colors.CRED}{0} Euro{colors.CEND}") # !!!ToDo!!!
print("")
print(f"(3) Monatliche Rente in Höhe von {monatliche_wunschrente} Euro ({colors.CRED}netto{colors.CEND}, progressiver persönlicher Einkommensteuersatz, verheiratet):")
print(f"=> Nötige monatliche Sparrate (konstant) = {colors.CRED}{0} Euro{colors.CEND}") # !!!ToDo!!!
print(f"=> Nötige monatliche Sparrate (muss jedes Jahr um {angenommene_inflationsrate_in_prozent}% erhöht werden) = {colors.CRED}{0} Euro{colors.CEND}") # !!!ToDo!!!
print("")
print("=> Vor- und Nachteile:")
print(f"(+) Genau wie bei der Dividenden-Strategie wird das in der Ansparphase angesparte Vermögen in der Rentephase nicht verzehrt, sondern erhalten.")
print(f"(+) Anders als bei der Dividenden-Strategie gibt es in der Ansparphase einen echten Zinseszinseffekt.")
print(f"(-) Anders als bei der Dividenden-Strategie beginnt das passive Einkommen erst mit Renteneintritt.")
print(f"(-) Genau wie bei der Dividenden-Strategie sind auch hier höhere Sparbeträge nötig, da das Kapital nicht verzehrt werden soll.")
print(f"(-) Es besteht eine Unsicherheit, wie im Jahr {renteneintritts_jahr} Kapitalerträge versteuert werden.")



# ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### #####
# ##### ##### ##### Vermögens-verzehrende Verrentungen: ##### ##### #####
# ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### #####

# Berechnungen Entnahmepläne:

angenommene_jaehrliche_rendite_entnahmeplan_in_prozent = 3.0 # (vgl. Handelsblatt vom 21.06.2024)

def vermoegens_verzehrung_konstante_entnahme(vermoegen, monatliche_entnahme):
	"""
	Gibt die Dauer (in Jahren) zurück, die das anegegbene Vermögen {vermoegen} bei einer (konstanten) monatlichen Entnhame von {monatliche_entnahme} hält.
	Annahme: Das Vermögen liegt ohne jegliche Verzinsung auf einem Konto.
	"""
	return vermoegen / (monatliche_entnahme * 12)

def vermoegens_verzehrung_steigende_entnahme(vermoegen, monatliche_entnahme, jaehrliche_steigerung_entnahme):
	"""
	Gibt die Dauer (in Jahren) zurück, die das anegegbene Vermögen {vermoegen} bei einer monatlichen Entnhame von {monatliche_entnahme} hält,
	welche allerdings jedes Jahr um {jaehrliche_steigerung_entnahme} steigt (um die Inflation auszugleichen).
	Annahme: Das Vermögen liegt ohne jegliche Verzinsung auf einem Konto.
	"""
	uebriges_vermoegen = vermoegen
	vergangene_monate = 0
	aktuelle_monatliche_entnahme = monatliche_entnahme
	while uebriges_vermoegen >= aktuelle_monatliche_entnahme:
		uebriges_vermoegen -= aktuelle_monatliche_entnahme
		vergangene_monate += 1
		if vergangene_monate % 12 == 0: # nachdem 12 Monate vergangen sind / vor Beginn eines neuen Jahres:
			aktuelle_monatliche_entnahme *= (1.0 + jaehrliche_steigerung_entnahme/100.0)
	return vergangene_monate / 12.0

def vermoegens_verzehrung_verzinster_entnahmeplan_konstante_entnahme(vermoegen, monatliche_entnahme, jaehrliche_rendite_entnahmeplan=angenommene_jaehrliche_rendite_entnahmeplan_in_prozent):
	"""
	Gibt die Dauer (in Jahren) zurück, die das anegegbene Vermögen {vermoegen} bei einer (konstanten) monatlichen Entnhame von {monatliche_entnahme} hält.
	Annahme: Das Vermögen liegt in einem verzinsten Entnahmeplan (z.B. aus Anleihen/Festgeld) mit einer Verzinsung von {jaehrliche_rendite_entnahmeplan} Prozent.
	Achtung: Steigt das Vermögen schneller als es entnommen wird, gibt diese Funktion Unendlich zurück!!!
	"""
	return vermoegens_verzehrung_verzinster_entnahmeplan_steigende_entnahme(vermoegen=vermoegen, monatliche_entnahme=monatliche_entnahme, jaehrliche_steigerung_entnahme=0.0, jaehrliche_rendite_entnahmeplan=jaehrliche_rendite_entnahmeplan)

def vermoegens_verzehrung_verzinster_entnahmeplan_steigende_entnahme(vermoegen, monatliche_entnahme, jaehrliche_steigerung_entnahme, jaehrliche_rendite_entnahmeplan=angenommene_jaehrliche_rendite_entnahmeplan_in_prozent):
	"""
	Gibt die Dauer (in Jahren) zurück, die das anegegbene Vermögen {vermoegen} bei einer monatlichen Entnhame von {monatliche_entnahme} hält,
	welche allerdings jedes Jahr um {jaehrliche_steigerung_entnahme} steigt (um die Inflation auszugleichen).
	Annahme: Das Vermögen liegt in einem verzinsten Entnahmeplan (z.B. aus Anleihen/Festgeld) mit einer Verzinsung von {jaehrliche_rendite_entnahmeplan} Prozent.
	Achtung: Steigt das Vermögen schneller als es entnommen wird, gibt diese Funktion Unendlich zurück!!!
	"""
	monatliche_rendite_entnahmeplan = 100.0 * ((1.0 + jaehrliche_rendite_entnahmeplan/100.0)**(1.0/12.0) - 1.0) # = 0,2466269772% bei 3,0% p.a. # = etwas weniger als 3,0% / 12,0 = 0,25%
	uebriges_vermoegen = vermoegen
	vergangene_monate = 0
	aktuelle_monatliche_entnahme = monatliche_entnahme
	while uebriges_vermoegen >= aktuelle_monatliche_entnahme:
		uebriges_vermoegen_alt = uebriges_vermoegen
		uebriges_vermoegen -= aktuelle_monatliche_entnahme # Das übrige Vermögen verringert sich jeden Monat um den monatlichen Entnahmebetrag...
		uebriges_vermoegen *= (1.0 + monatliche_rendite_entnahmeplan/100.0) # ...da sich das Vermögen allerdings auch in einem verzinsten Entnahmeplan befindet, so erhöht sich das übrige Vermögen auch jeden Monat wieder etwas. # (lasse das Vermögen sich erst nach der 1. Entnahme vermehren!)
		if uebriges_vermoegen > uebriges_vermoegen_alt: # Das Vermögen ist so gut verzinst, dass es durch die regelmäßigen Entnahmen gar nicht sinkt, sondern steigt...
			return float("inf") # ...gebe Unendlich zurück, da das Vermögen so unendlich lange "hält"!
		vergangene_monate += 1
		if vergangene_monate % 12 == 0: # nachdem 12 Monate vergangen sind / vor Beginn eines neuen Jahres:
			aktuelle_monatliche_entnahme *= (1.0 + jaehrliche_steigerung_entnahme/100.0)
	return vergangene_monate / 12.0

print("")
print(colors.CGREEN + "##### ##### ##### Vermögens-verzehrende Verrentungen: ##### ##### #####" + colors.CEND)

# ##### Besparen des MSCI World, monatliche Entnahme der Rente, Verzehrung des Vermögens: #####
print("")
print(colors.CGREEN + "##### Besparen des MSCI World, monatliche Entnahme der Rente, Verzehrung des Vermögens: #####" + colors.CEND)
print(f"Nehmen wir nun erneut an, dass du mit deinen monatlichen Sparbeiträgen einen ETF auf den MSCI World (oder einen vergleichbaren Fond) besparst (Sparplan).")
print(f"Nehmen wir ferner erneut an, dass der MSCI World eine jährliche Rendite von {msci_world_rendite}% abwirft.")
print(f"Schließlich nehmen wir an, dass du in deiner Rentenphase jeden Monat deine Rente in Höhe von {monatliche_wunschrente} Euro (brutto/netto je nach Betrachtung, s.u.) durch den Verkauf von Anteilen entnimmst " +\
	f"und dass sich dein angespartes Vermögen dadurch allmählich verringert, also verzehrt(!) wird, bis es schließlich im Alter von {lebenserwartung} Jahren aufgebraucht ist.")
print(f"Wir nehmen entweder an, dass (a) kein Inflationsausgleich in der Rentenphase stattfinden soll, dass die in der Rentenphase entnommene monatliche Rente also konstant bleibt und im Fall (b) dass sich deine monatlich entnomme Rente jedes Jahr um {angenommene_inflationsrate_in_prozent}% als Inflationsausgleich erhöht.")
print(f"Ferner gehen wir entweder davon aus, dass du keinen separaten Entnahmeplan durchführst, die Rente also direkt durch regelmäßige Verkäufe deiner ETF-Anteile realisierst.")

# (a) Ohne Inflationsausgleich (d.h. konstante Entnahme in der Rentenphase):

print("")
print("(a) Es soll kein(!) Inflationsausgleich in der Rentenphase stattfinden, die in der Rentenphase entnommene monatliche Rente bleibt konstant:")
print("")
print(f"(0) Monatliche Rente in Höhe von {monatliche_wunschrente} Euro ({colors.CGREEN}brutto{colors.CEND}):")

# 1. Frage: Wie hoch muss mein angespartes Vermögen zum Renteneintritt sein, um daraus meine Wunschrente verzehren zu können?:
notwendiges_vermoegen_fuer_msci_verzehrende_monatliche_entnahme_strategie = funktion_invertieren(vermoegens_verzehrung_verzinster_entnahmeplan_konstante_entnahme, dauer_rentenphase_in_jahren, "vermoegen", {"monatliche_entnahme": monatliche_wunschrente, "jaehrliche_rendite_entnahmeplan": msci_world_rendite}, praezision=0.1, initialer_schaetzwert=10000)

print(f"Zum Renteneintritt musst du ein Vermögen von {notwendiges_vermoegen_fuer_msci_verzehrende_monatliche_entnahme_strategie} Euro im MSCI World angespart haben, um danach deine (mit der Inflation NICHT mitwachsende konstante) Rente in Höhe von {monatliche_wunschrente} Euro (brutto) verzehrend entnehmen zu können.")

# 2. Frage: Wie hoch muss meine monatliche Sparrate (konstant oder mit Inflation wachsend) sein, um am Ende der Ansparphase das in 1. errechnete Vermögen angespart zu haben?:
notwendige_konstante_monatliche_sparrate_fuer_msci_verzehrende_monatliche_entnahme_strategie = (1.0/12.0) * funktion_invertieren(sparplan_ausfuehren, notwendiges_vermoegen_fuer_msci_verzehrende_monatliche_entnahme_strategie, "sparrate_initial", {"sparrate_steigerungsrate": 1.00, "wertsteigerung_anlageobjekt": 1.00 + (msci_world_rendite/100.0), "anlage_dauer": dauer_sparphase_in_jahren})
notwendige_wachsende_monatliche_sparrate_fuer_msci_verzehrende_monatliche_entnahme_strategie = (1.0/12.0) * funktion_invertieren(sparplan_ausfuehren, notwendiges_vermoegen_fuer_msci_verzehrende_monatliche_entnahme_strategie, "sparrate_initial", {"sparrate_steigerungsrate": 1.00 + (angenommene_inflationsrate_in_prozent/100.0), "wertsteigerung_anlageobjekt": 1.00 + (msci_world_rendite/100.0), "anlage_dauer": dauer_sparphase_in_jahren})

print(f"=> Nötige monatliche Sparrate (konstant) = {colors.CGREEN}{notwendige_konstante_monatliche_sparrate_fuer_msci_verzehrende_monatliche_entnahme_strategie} Euro{colors.CEND}")
print(f"=> Nötige monatliche Sparrate (muss jedes Jahr um {angenommene_inflationsrate_in_prozent}% erhöht werden) = {colors.CGREEN}{notwendige_wachsende_monatliche_sparrate_fuer_msci_verzehrende_monatliche_entnahme_strategie} Euro{colors.CEND}")
print("")
print(f"(1) Monatliche Rente in Höhe von {monatliche_wunschrente} Euro ({colors.CGREEN}netto{colors.CEND}, {kapitalertragssteuer_in_prozent}% Kapitalertragssteuer, {freibetrag_in_euro} Euro Freibetrag):")
print(f"=> Nötige monatliche Sparrate (konstant) = {colors.CGREEN}{0} Euro{colors.CEND}") # !!!ToDo!!!
print(f"=> Nötige monatliche Sparrate (muss jedes Jahr um {angenommene_inflationsrate_in_prozent}% erhöht werden) = {colors.CGREEN}{0} Euro{colors.CEND}") # !!!ToDo!!!
print("")
print(f"(2) Monatliche Rente in Höhe von {monatliche_wunschrente} Euro ({colors.CGREEN}netto{colors.CEND}, progressiver persönlicher Einkommensteuersatz, ledig):")
print(f"=> Nötige monatliche Sparrate (konstant) = {colors.CGREEN}{0} Euro{colors.CEND}") # !!!ToDo!!!
print(f"=> Nötige monatliche Sparrate (muss jedes Jahr um {angenommene_inflationsrate_in_prozent}% erhöht werden) = {colors.CGREEN}{0} Euro{colors.CEND}") # !!!ToDo!!!
print("")
print(f"(3) Monatliche Rente in Höhe von {monatliche_wunschrente} Euro ({colors.CGREEN}netto{colors.CEND}, progressiver persönlicher Einkommensteuersatz, verheiratet):")
print(f"=> Nötige monatliche Sparrate (konstant) = {colors.CGREEN}{0} Euro{colors.CEND}") # !!!ToDo!!!
print(f"=> Nötige monatliche Sparrate (muss jedes Jahr um {angenommene_inflationsrate_in_prozent}% erhöht werden) = {colors.CGREEN}{0} Euro{colors.CEND}") # !!!ToDo!!!

# (b) Mit Inflationsausgleich (d.h. steigende Entnahme in der Rentenphase):

print("")
print(f"(b) Es soll ein Inflationsausgleich in der Rentenphase stattfinden, deine monatlich entnomme Rente soll jedes Jahr um {angenommene_inflationsrate_in_prozent}% als Inflationsausgleich erhöht werden:")
print("")
print(f"(0) Monatliche Rente in Höhe von {monatliche_wunschrente} bis {noetige_inflationsangepasste_rente_zum_rentenende} Euro ({colors.CGREEN}brutto{colors.CEND}):")

notwendiges_vermoegen_fuer_msci_verzehrende_monatliche_entnahme_strategie_mit_inflationsausgleich = funktion_invertieren(vermoegens_verzehrung_verzinster_entnahmeplan_steigende_entnahme, dauer_rentenphase_in_jahren, "vermoegen", {"monatliche_entnahme": monatliche_wunschrente, "jaehrliche_steigerung_entnahme": angenommene_inflationsrate_in_prozent, "jaehrliche_rendite_entnahmeplan": msci_world_rendite}, praezision=0.1, initialer_schaetzwert=10000)

print(f"Zum Renteneintritt musst du ein Vermögen von {notwendiges_vermoegen_fuer_msci_verzehrende_monatliche_entnahme_strategie_mit_inflationsausgleich} Euro im MSCI World angespart haben, um danach deine (mit der Inflation mitwachsende) Rente in Höhe von zunächst {monatliche_wunschrente} Euro (brutto) verzehrend entnehmen zu können.")

notwendige_konstante_monatliche_sparrate_fuer_msci_verzehrende_monatliche_entnahme_strategie_mit_inflationsausgleich = (1.0/12.0) * funktion_invertieren(sparplan_ausfuehren, notwendiges_vermoegen_fuer_msci_verzehrende_monatliche_entnahme_strategie_mit_inflationsausgleich, "sparrate_initial", {"sparrate_steigerungsrate": 1.00, "wertsteigerung_anlageobjekt": 1.00 + (msci_world_rendite/100.0), "anlage_dauer": dauer_sparphase_in_jahren})
notwendige_wachsende_monatliche_sparrate_fuer_msci_verzehrende_monatliche_entnahme_strategie_mit_inflationsausgleich = (1.0/12.0) * funktion_invertieren(sparplan_ausfuehren, notwendiges_vermoegen_fuer_msci_verzehrende_monatliche_entnahme_strategie_mit_inflationsausgleich, "sparrate_initial", {"sparrate_steigerungsrate": 1.00 + (angenommene_inflationsrate_in_prozent/100.0), "wertsteigerung_anlageobjekt": 1.00 + (msci_world_rendite/100.0), "anlage_dauer": dauer_sparphase_in_jahren})

print(f"=> Nötige monatliche Sparrate (konstant) = {colors.CGREEN}{notwendige_konstante_monatliche_sparrate_fuer_msci_verzehrende_monatliche_entnahme_strategie_mit_inflationsausgleich} Euro{colors.CEND}")
print(f"=> Nötige monatliche Sparrate (muss jedes Jahr um {angenommene_inflationsrate_in_prozent}% erhöht werden) = {colors.CGREEN}{notwendige_wachsende_monatliche_sparrate_fuer_msci_verzehrende_monatliche_entnahme_strategie_mit_inflationsausgleich} Euro{colors.CEND}")
print("")
print(f"(1) Monatliche Rente in Höhe von {monatliche_wunschrente} bis {noetige_inflationsangepasste_rente_zum_rentenende} Euro ({colors.CGREEN}netto{colors.CEND}, {kapitalertragssteuer_in_prozent}% Kapitalertragssteuer, {freibetrag_in_euro} Euro Freibetrag):")
print(f"=> Nötige monatliche Sparrate (konstant) = {colors.CGREEN}{0} Euro{colors.CEND}") # !!!ToDo!!!
print(f"=> Nötige monatliche Sparrate (muss jedes Jahr um {angenommene_inflationsrate_in_prozent}% erhöht werden) = {colors.CGREEN}{0} Euro{colors.CEND}") # !!!ToDo!!!
print("")
print(f"(2) Monatliche Rente in Höhe von {monatliche_wunschrente} bis {noetige_inflationsangepasste_rente_zum_rentenende} Euro ({colors.CGREEN}netto{colors.CEND}, progressiver persönlicher Einkommensteuersatz, ledig):")
print(f"=> Nötige monatliche Sparrate (konstant) = {colors.CGREEN}{0} Euro{colors.CEND}") # !!!ToDo!!!
print(f"=> Nötige monatliche Sparrate (muss jedes Jahr um {angenommene_inflationsrate_in_prozent}% erhöht werden) = {colors.CGREEN}{0} Euro{colors.CEND}") # !!!ToDo!!!
print("")
print(f"(3) Monatliche Rente in Höhe von {monatliche_wunschrente} bis {noetige_inflationsangepasste_rente_zum_rentenende} Euro ({colors.CGREEN}netto{colors.CEND}, progressiver persönlicher Einkommensteuersatz, verheiratet):")
print(f"=> Nötige monatliche Sparrate (konstant) = {colors.CGREEN}{0} Euro{colors.CEND}") # !!!ToDo!!!
print(f"=> Nötige monatliche Sparrate (muss jedes Jahr um {angenommene_inflationsrate_in_prozent}% erhöht werden) = {colors.CGREEN}{0} Euro{colors.CEND}") # !!!ToDo!!!
print("")
print("=> Vor- und Nachteile:")
print(f"(+) Dadurch dass das Vermögen verzehrt wird, muss weniger angespart werden.")
print(f"(+) Anders als bei der Dividenden-Strategie gibt es in der Ansparphase einen echten Zinseszinseffekt.")
print(f"(-) Das Vermögen wird verzehrt und ist am Ende aufgebraucht.")

# ##### Besparen des MSCI World, zweimalige Entnahme der Rente (einmal zu Rentenbeginn und einmal während der Rente), Verzehrung des Vermögens: #####
print("")
print(colors.CGREEN + "##### Besparen des MSCI World, zweimalige Entnahme der Rente (einmal zu Rentenbeginn und einmal während der Rente), Verzehrung des Vermögens: #####" + colors.CEND)
print("ToDo")
print("=> Vor- und Nachteile:")
print(f"(+) Größere Sicherheit bezüglich Kursschwankungen: man kennt seine genaue Rentenhöhe.")
print(f"(+) Anders als bei der Dividenden-Strategie gibt es in der Ansparphase einen echten Zinseszinseffekt.")
print(f"(-) Das auf einen Schlag entnommene Vermögen kann sich nicht mehr weiter unter dem Zinseszinseffekt vermehren (in der Rentenphase).")
print(f"(-) Das Vermögen wird verzehrt und ist am Ende aufgebraucht.")

# ##### Besparen des MSCI World, einmalige Entnahme der Rente (zu Rentenbeginn), Verzehrung des Vermögens: #####
print("")
print(colors.CGREEN + "##### Besparen des MSCI World, einmalige Entnahme der Rente (zu Rentenbeginn), Verzehrung des Vermögens: #####" + colors.CEND)
print("ToDo")
print("=> Vor- und Nachteile:")
print(f"(+) Größere Sicherheit bezüglich Kursschwankungen: man kennt seine genaue Rentenhöhe.")
print(f"(-) Das auf einen Schlag entnommene Vermögen kann sich nicht mehr weiter unter dem Zinseszinseffekt vermehren.")
print(f"(-) Das Vermögen wird verzehrt und ist am Ende aufgebraucht.")

# ##### Eine Privatrente mit 1,00 Prozent Effektivkosten und einmaliger Kapitalzahlung: #####
print("")
print(colors.CGREEN + "##### Eine Privatrente mit 1,00 Prozent Effektivkosten und einmaliger Kapitalzahlung: #####" + colors.CEND)
print("ToDo")
print("=> Vor- und Nachteile:")
print(f"(+) Steuervorteil: Es muss nur 50% des Gewinns mit dem persönlichen Einkommensteuersatz versteuert werden. Dies könnte insb. dann interessant werden, falls die Politik die pauschale Kapitalertragssteuer abschaffen sollte.")
print(f"(+) Umschichtungen des Portfolios (Rebalancing) während der Ansparphase sind ohne Zahlung von Steuern möglich.")
print(f"(-) Gebühren der Versicherung")

# ##### Eine Privatrente mit 0,50 Prozent Effektivkosten und einmaliger Kapitalzahlung: #####
print("")
print(colors.CGREEN + "##### Eine Privatrente mit 0,50 Prozent Effektivkosten und einmaliger Kapitalzahlung: #####" + colors.CEND)
print("ToDo")
print("=> Vor- und Nachteile:")
print(f"(+) Steuervorteil: Es muss nur 50% des Gewinns mit dem persönlichen Einkommensteuersatz versteuert werden. Dies könnte insb. dann interessant werden, falls die Politik die pauschale Kapitalertragssteuer abschaffen sollte.")
print(f"(+) Umschichtungen des Portfolios (Rebalancing) während der Ansparphase sind ohne Zahlung von Steuern möglich.")
print(f"(-) Gebühren der Versicherung")

