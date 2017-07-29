import requests
from pyquery import PyQuery
import re
import time
#import numpy
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By


def urlMaker(page, filters=None):
    if filters is None:
        filters = {}
    base = 'http://www.wg-gesucht.de/wg-zimmer-in-Muenchen.90.0.1.'
    base_end = '.html'
    url = base + str(page) + base_end + (
        '' if not len(filters.keys()) else '?' + '&'.join([str(k) + '=' + str(v) for k, v in filters.items()]))
    return url


pat = re.compile('liste-details-ad-\\d+')


def iterfun(element):
    if pat.fullmatch(str(element.attr('id'))):
        return element('.detailansicht').attr['href']
    return


def query(url):
    page = requests.get(url)
    query = PyQuery(page.text)
    results = []
    q = query('#main_column').children().filter('div').items()
    for i in q:
        tmp = iterfun(i)
        if tmp is not None:
            results.append(tmp)
    return results


def get_num(x):
    return ''.join(ele for ele in x if ele.isdigit() or ele == '')


# idNr = 'https://www.wg-gesucht.de/nachricht-senden.html?id=' + get_num(results[i]) '''getnum on results[i]'''

# here you can put which page/page Nrs to go through, 0->page 1, 1->page 2
# 1 = herr
# 2 = frau
def fillForm(vorname, nachname, email, text, geschlecht, pageNr):
    q = query(urlMaker(pageNr))
    for i in range(0, len(q)):
        print('Applying for ' + vorname + ' to this WG: ' + q[i])
        pnr = get_num(q[i])
        if int(pnr) < 9999999 and int(pnr)>999999:
            idNr = str('https://www.wg-gesucht.de/nachricht-senden.html?id=' + pnr)
            driver = webdriver.Firefox() #Firefox()
 #           fp = webdriver.FirefoxProfile()
#            fp.set_preference("network.cookie.cookieBehavior", 2)
#            driver = webdriver.Firefox(firefox_profile=fp)
            driver.get(idNr)                      
            python_button = driver.find_elements_by_xpath("//input[@name='sicherheit_bestaetigung']")[0]
            python_button.click()
            print('page opened') 
            driver.find_element_by_id('cookie-confirm').click()
            driver.find_element_by_name('nachricht').send_keys(text)
            my_select = Select(driver.find_element_by_name('u_anrede'))
            my_select.select_by_index(geschlecht)
            driver.find_element_by_name('vorname').send_keys(vorname)
            driver.find_element_by_name('nachname').send_keys(nachname)
            driver.find_element_by_name('email').send_keys(email)
            driver.find_element_by_id('kopieanmich').click()
 #           driver.save_screenshot('filled')
            
            driver.find_element_by_css_selector('input.loadWait.btn.btn-block.btn-md.btn-orange').click()
            print('Application Filled & Sent')
            driver.close()

        else:
            pass



def main():
    xi = """Hello, I'm Julie from China planning to go to Technical University Munich to pursue my Master's degree in October. I'm 23 and want to find a furnished place to live in Munich from September or earlier.

I'm a calm and nice girl and pay attention to hygiene. If you rent your apartment or room to me, I'll keep it in good state:) Besides, I have got a full scholarship from my country to support my living and study in Munich, so you don't have to worry about my income. 

I'm fond of traveling and like to get to know different culture and people. Flatshare is a good way to make new friends and know different culture. I'm a good cook who can cook delicious Chinese food. Maybe my future flatmate(s) and I can try each other's traditional food :)
I would like to get an appointment from you if possible, via Skype because I will be in my home country for the next 2 Weeks.
Hoping to hear from you soon.""" 

    maximillian =  """Hallo liebe hoffentlich zukünftige Mitbewohner,

ich bin der Max, 22 Jahre alt, und gerade BWL student in München. Davor habe ich ein Praktikum in Berlin gemacht, bin dann zurück fürs Studium nach München und komme gerade von einem Erasmussemester in London zurück. Bis jetzt hab ich bei meinen Eltern gewohnt, wo ich endlich raus muss, und suche daher eine nette WG. 
Bezüglich WG-Leben bin ich flexibel und komme mit vielem zurecht. Ich kann mich an einen strikten Putzplan halten, es stört mich aber auch nicht, wenn jemand mal bisschen unordentlicher ist als ich. Zu mir: persönlich am wichtigsten sind mir meine Freunde, Essen und Musik, ansonsten bin ich an allerlei Dingen interessiert und auch für vieles zu begeistern. Eigentlich bin ich eher ruhig, aber wenn es passt auch gerne für Action zu haben. Ich fände es cool, ein reges WG-Leben zu führen, man muss allerdings ja auch nichts erzwingen.
MFG,
Maximillian Eisenrieder"""
    mandy = """Hallo :) mein Name ist Mandy und ich bin 21 Jahre alt. Ich suche ab August oder später nach einer WG in München, vorzugsweise nicht allzu weit weg vom Zentrum. Ich fange nämlich im Oktober ein Medizinstudium an der LMU an. 
Ich bin sehr aufgeschlossen, freundlich und abenteuerlustig. In meiner Freizeit treibe ich gerne Sport (meistens Beach Volleyball und Radeln) oder gehe auch gern mit Freunden wandern. Ich würde mich freuen eine WG zu finden, in der sich alle super verstehen und man auch ab und zu mal etwas zusammen unternimmt, sei es ein kleiner Ausflug an die Isar, eine Mass im Biergarten oder ein Kochabend, ich wäre jedenfalls dabei! Ich bin außerdem ein sehr offener Mensch und freue mich immer wieder neue Menschen kennenzulernen.
Die Zeit nach meinem Abi habe ich erst mit ein wenig Arbeiten verbracht, um dann auf einer Farm in Kanada zu leben und danach dann ein Lehramtstudium an der LMU zu beginnen, was ich aber jetzt beendet habe. Momentan lebe ich in Neufahrn, arbeite in einem bayrischen Wirtshaus in München und mache noch einen Japanischkurs.

Ich hätte demnächst auch Zeit und Lust mir die WG einmal anzuschauen und euch dabei kennenzulernen. 
Wenn ihr also ein Zimmer für mich habt und mich näher kennenlernen möchtet, freue ich mich auf eine Nachricht :) 

Bis dahin, liebe Grüße

Mandy :)"""
    mike = """Ich bin 20 Jahre alt und fange an masters Physik an der TUM zu studieren. Urspinglich komme ich aus Portland, Oregon. Mein großvater war Deutsch us es hat mich motiviert nach Deutschland zu kommen. Mit mir kann man viel Spaß haben, immer gut gelaunt, koche sehr gerne und bin für jede Party zu haben. In meiner Freizeit fliege ich Modellflugzeuge und wenn es der innere Schweinehund mal wieder geschafft hab geh ich auch recht gern laufen.
Als Mitbewohner bin ich meiner Meinung nach recht unkompliziert, spreche alles immer direkt an und finde es auch wichtig mir alles direkt zu sagen damit man eine Lösung finden kann. Wg erfahrung hab ich 4 Jahre in mein Fraternity in Univery of Chicago gesammelt, wo ich Physik Baechlors Studiert habe. Ich bin absolut kein Fan einer Zweck-WG, man lebt ja schließlich zusammen, deswegen würde ich mich riesig auf ein abendliche Bier freuen!
Falls ihr Interesse habt würde ich mich riesig über eine Antwort Freuen! Ich bin Fliege nächste Woche nach München und daher bin ich ab 1. August om München.
Cheers,
Mike"""
    raj = """Ich bin Raj. Ich komme aus Indien und ich lerne Deutsche sprache in Heidelberg, ich fange an in Septermber Physik Master an der LMU zu studieren. Ich habe ihren werbung gesehen und das
ist mir gefallen. Ich habe bisher mit eine Deutsche gast familie gewohnt 
aber die antrag hat beendet. Ich möchte gern in WG leben erfahren, ich bin sehr freundlich und hilfsbereit... In mein freizeit lese ich bücher, koche, reise und mache was mein Freunden.
Kann ich ein besichtigungstermin  von euch haben?

Herzlich Gruße"""
    leo = """Servus beinand,

i bin da Lepi und kimm ausam Dorf bei Rosenheim. Ab September dat i mitam Kirchenmusikstudium an da Musikhochschui ofanga, weil i sau gern Orgel spui und sing (am liebstn Bach).

Seitram Joa versuach i vegan z lebn. Mia wars dewegn recht, wenn bei uns in da Küch as Essn trennt werd.

In meina Freizeit geh i Dienstags kegeln und danoch an Stammtisch. Sunst bin i Vorstand in da Katholischen Landjugendbewegung (KLJB) und ge vui gern zum Voiksdanz.

Natürlich kimm i asram zinftigm Elternhaus bin deswegn a ordentlicha Kerl. I dat ma wünschn, dass Ihr Schafkopf spuin kennts, damit ma uns unta da Woch amoi anam gmiadlichn Omnd af a Mass zamsetzn kenna.

Wennds nexde Woch zeit hobts kimm i gern afan Besichtigungtermin vorbei.


LG

Leopold Wimmer
 """
    
    for i in range(0,1):               
 #       time.sleep(14)
 #       fillForm('Maximillian', 'Eisenrieder', 'neo.master1@yandex.com', maximillian, 1, i)
#        time.sleep(13)
        fillForm('Mandy', 'Schwab', 'mandy.schwab1@web.de', mandy, 2, i)
#         time.sleep(12)
        fillForm('Mike', 'Zimmerman', 'zimmerman.mike1@web.de', mike, 1, i)       
        fillForm('Raj', 'Singh', 'raj.issingh95@gmail.com', raj, 1, i)
        fillForm('Leopold', 'Wimmer', 'leopold-wimmer@web.de', leo, 1,i)
        fillForm('Xi', 'Wang', 'xiwang764891@126.com', xi, 2,i) 
        
main()
