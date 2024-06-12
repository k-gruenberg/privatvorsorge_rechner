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

def funktion_invertieren(funktion, funktionswert, name_zu_bestimmender_parameter, uebrige_parameter, praezision=0.01):
	param_estimate = 1
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
kapitalertragssteuer_in_prozent = 26.3750
freibetrag_in_euro = 1000
print(f"Monatliche Rente in Höhe von {monatliche_wunschrente} Euro ({colors.CRED}netto{colors.CEND}, {kapitalertragssteuer_in_prozent}% Kapitalertragssteuer, {freibetrag_in_euro} Euro Freibetrag):")
print(f"=> Hypothetische obere Schranke der monatlichen Sparrate = x Euro") # ToDo
print(f"=> Nötige monatliche Sparrate (konstant) = {colors.CRED}x Euro{colors.CEND}") # ToDo
print(f"=> Nötige monatliche Sparrate (muss jedes Jahr um {angenommene_inflationsrate_in_prozent}% erhöht werden) = {colors.CRED}x Euro{colors.CEND}") # ToDo
print(f"=> Beachte hierbei, dass mit der Zeit auch dein passives Dividenden-Einkommen steigt. Du kannst dieses natürlich zur Tilgung deiner Sparrate verwenden, also reinvestieren!")
print("")
print("=> Vor- und Nachteile:")
print(f"(+) Vorteilhaft ist, dass zu erwarten ist, dass sich die Dividenden, also deine Rente, auch in deiner Rentenzeit erhöhen und an die Inflation anpassen werden.")
print(f"(+) Du hast bereits vor Rentenbeginn ein passives Einkommen!")
print(f"(+) Außerdem kannst du deine Dividendenaktien/-fonds problemlos vererben (abzüglich Erbschaftssteuer von 7-30 %, der Freibetrag liegt hier bei 500.000 Euro für Ehegatten und 400.000 Euro für Kinder).")
print(f"(-) Nachteilhaft ist, dass Dividenden Schwankungen unterliegen und in Krisenzeiten auch mal ganz ausfallen können. Eine Diversifizierung der Dividenden-Aktien ist dringend anzuraten!")
print(f"(-) Außerdem ist die Wertsteigerung von Dividenden-Aktien i.d.R. gering, wodurch kein Zinseszinseffekt eintritt und sehr hohe Summen in der Ansparphase angespart werden müssen!")

# ##### Besparen des MSCI World, regelmäßige Entnahme, unter Erhalt des Vermögens: #####
print("")
print(colors.CRED + "##### Besparen des MSCI World, regelmäßige Entnahme, unter Erhalt des Vermögens: #####" + colors.CEND)
print("ToDo")
print("=> Vor- und Nachteile:")
print(f"(+) Genau wie bei der Dividenden-Strategie wird das in der Ansparphase angesparte Vermögen in der Rentephase nicht verzehrt, sondern erhalten.")
print(f"(+) Anders als bei der Dividenden-Strategie gibt es in der Ansparphase einen echten Zinseszinseffekt.")
print(f"(-) Anders als bei der Dividenden-Strategie beginnt das passive Einkommen erst mit Renteneintritt.")



# ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### #####
# ##### ##### ##### Vermögens-verzehrende Verrentungen: ##### ##### #####
# ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### #####
print("")
print(colors.CGREEN + "##### ##### ##### Vermögens-verzehrende Verrentungen: ##### ##### #####" + colors.CEND)

# ##### Besparen des MSCI World, monatliche Entnahme der Rente, Verzehrung des Vermögens: #####
print("")
print(colors.CGREEN + "##### Besparen des MSCI World, monatliche Entnahme der Rente, Verzehrung des Vermögens: #####" + colors.CEND)
print("ToDo")
print("=> Vor- und Nachteile:")
print(f"(+) Dadurch dass das Vermögen verzehrt wird, muss weniger angespart werden.")
print(f"(-) Das Vermögen wird verzehrt und ist am Ende aufgebraucht.")

# ##### Besparen des MSCI World, zweimalige Entnahme der Rente (einmal zu Rentenbeginn und einmal während der Rente), Verzehrung des Vermögens: #####
print("")
print(colors.CGREEN + "##### Besparen des MSCI World, zweimalige Entnahme der Rente (einmal zu Rentenbeginn und einmal während der Rente), Verzehrung des Vermögens: #####" + colors.CEND)
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

