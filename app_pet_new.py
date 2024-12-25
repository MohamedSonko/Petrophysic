import streamlit as st
from nltk.chat.util import Chat, reflections

# Define your chatbot pairs
pairs = [
    ["(Bonjour|Salut|Comment allez-vous?|Comment vas-tu?|Comment ça va?|Bonsoir|Bon après-midi)", 
     ["Salut je suis MLS, le pétrophysicien, que puis-je faire pour vous?"]],
    ["(Qu'est-ce qu'une diagraphie?|C'est quoi une diagraphie?)", 
     ["Les diagraphies sont des enregistrements des paramètres physiques des formations traversées au cours du forage.Ces enregistrements sont matérialisés par des courbes et nous distinguons deux types de diagraphies:\nDiagraphies instantanées ou LWD (Logging While Drilling): mesurées au cours du forage (de haut en bas)\nDiagraphies différées ou wireline: mesurées après le forage (de bas en haut)"]],
    ["Quels sont les types de diagraphies?", 
     ["Les différents types de diagraphie sont:\nles diagraphies de porosité: Sonic, Densité et Neutron\nles diagraphies de lithologie: Gamma Ray (GR), Photoélectique (PEF) et Potentiel Spontané (PS)\nles diagraphies de trou: Caliper et CBL\nles diagraphies de résistivité: Dispositif normal (16 inches et 64 inches), Dispositif latéral, Logs électrodes focalisés (LLD, LLS, Laterolog 3, HRLA), Induction logs (ILD, ILM, AIT), MSFL, Microlog, MicroLaterolog"]],
    ["(.*) zones d'hydrocarbures", 
     ["Les hydrocarbures peuvent être détectés en analysant conjointement les courbes de résistivité, de densité et de neutron:\nune forte valeur de la résistivité combinée au croisement des courbes de densité et de neutron avec une augmentation de la densité et une diminution du neutron prouve la présence d'hydrocarbure à la profondeur indiquée"]],
    ["(.*) zone d'eau", 
     ["L'eau peut être détectée en analysant conjointement les courbes de résistivité, de densité et de neutron: \nune faible valeur de la résitivité combinée au croisement des courbes de densité et de neutron avec une augmentation de la densité et une diminution du neutron"]],
    ["Comment calculer la porosité?", 
     ["La porosité est calculée à partir des courbes de porosité, comme suit:\nA partir du Sonic: PHI = (delta log - delta matrice) / (delta fluide - delta matrice) avec delta ma: temps de transit de la matrice et delta tf: temps de transit du fluide (189μs/ft)\nA partir de la Densité: PHI = (densité lue - densité matrice) / (densité fluide - densité matrice) avec ρma(2.65 pour les sables, 2.68 pour les sables calcaires, 2.71 pour les calcaires et 2.87 pour les dolomies) et ρf(1 pour l'eau potable, 1.1 pour l'eau salée, 0.735 pour l'eau avec un pourcentage de gaz résiduel, 0.92 pour l'eau avec un pourcentage d'huile)\nA partir du Neutron (lecture de la courbe)\nA partir de la combinaison Neutron-Densité: PHI = (PHId + PHIn) / 2 (pour les liquides) et PHI = (((PHId)^2 + (PHIn)^2) / 2)^(1/2) (pour le gaz)"]],
    ["(.*) saturation en hydrocarbures", 
     ["La saturation en hydrocarbures peut être calculée en soustrayant la saturation en eau de la saturation totale en fluide (eau + hydrocarbures) qui vaut 1 (en termes de fraction) ou 100 (en termes de pourcentage)"]],
    ["(.*) saturation en eau", 
     ["La saturation en eau peut être calculée à partir des formules suivantes:\nA partir de la formule d'Archie: Sw = ((a * Rw) / (PHIe^m * Rt))^(1/2) avec a(tortuosité), m(cimentation), n(facteur de saturation), PHIe(porosié effective), Rw(résistivité de l'eau), Rt(résistivité totale)\nA partir de la formule de Simandoux: Sw = ((D^2 + E)^0.5 - D)^(2/n) avec C = (1 - Vsh) * a * Rw / PHIe^m, D = (C * Vsh) / (2 * Rsh), E = C / Rt, m(cimentation), n(facteur de saturation), PHIe(porosité effective), Rt (résistivité totale), Rw(résistivité de l'eau), Rsh (résistivité de l'argile), Vsh (volume d'argile)\nA partir de la formule de Waxman-Smits: Sw=(PHIt^(-m')*Rw/Rt(1+(RwBQv/Sw0)) )^(1/n') avec Sw0(saturation en eau initiale),porosité totale obtenue à partir de la courbe densité, Rw(résistivité de l'eau),B(conductancecationique équivalente),Qt(concentration de l'échange des cations hydratés), Rt(résistivité totale),m'(exposant de la cimentation Waxman),n'(exosant de la saturation Waxman)\nA partir de la formule Dual Water:Sw=(PHIt^(-m)*Rw/Rt(1-(Swb*Rw/Sw0)*((1/Rwb)-(1/Rw))) )^(1/n) avec Sw0(saturation en eau initiale),porosité totale obtenue à partir de la courbe de densité, Rw(résistivité de l'eau), Rt(résistivité totale), m(cimentation),n(exposant de la saturation),Swb=((Vsh*PHITsh)/(PHIT)),Rwb=(Rsh*(PHITsh)^m)\nA partir de la formule d'Istvan Juhasz:Sw=(PHIt^(-m')*Rw/Rt(1+((Qvn*Rw)/Sw0)*((1/Rwsh)-(1/Rw))) )^(1/n' ) avec Sw0(saturation en eau initiale), porosité obtenue à partir de la courbe de densité, Rw(résistivité de l'eau),Rt(résistivité totale),m'(exposant cimentation Waxman),n'(exposant saturation Waxman),Qvn=(Vsh*PHITsh)/PHIT,Rwsh=(Rsh*(PHITsh)^m)"]],
    ["(.*) perméabilité", 
     ["La perméabilité peut être calculée comme suit:\nA partir de la formule de Coates et Dumanoir: K = (70 * PHIe^2 * (1 - Swirr) / Swirr)^2 avec PHIe(porosité effective), Swirr(saturation en eau irréductible)\nA partir de la formule de Timur: K = (100 * PHIe^2.25 / Swirr)^2 avec PHIe(porosité effective), Swirr(saturation en eau irréductible)\nA partir de la formule de Tixier: K = (250 * PHIe^3 / Swirr)^2 avec PHIe(porosité effective), Swirr(saturation en eau irréductible)"]],
    ["(.*) volume d'argile", 
     ["Le volume d'argile peut être calculé comme suit:\nA partir du Gamma Ray: Vsh = (GR - GRcl) / (GRsh - GRcl) avec GR(valeur lue à une profondeur donnée), GRcl(valeur dans les sables propres), GRsh(valeur dans les intervalles 100% argile)\nA partir du Potentiel Spontané: Vsh = (PS - PScl) / (PSsh - PScl) avec PS(valeur lue à une profondeur donnée), PScl(valeur dans les sables propres), PSsh(valeur dans les zones 100% argile)\nA partir de la combinaison Neutron-Densité:Vsh=(PHIn-PHId)/(PHInsh-PHIdsh) avec Øn(porosité du neutron dans la zone d'intérêt),Ød(porosité de la densité dans la zone d'intérêt),Ønsh(porosité du neutron dans la zone 100% argile),Ødsh(porosité de la densité dans la zone 100% argile)\nA partir du modèle Thomas-Stieber (modèle graphique)"]],
    ["(Merci|Au revoir|A bientôt|Merci beaucoup|Ciao|Bye)",
     ["Je vous en prie...A bientôt"]]
]

# Create a chatbot class
class Chatbot:
    def __init__(self, pairs, reflections):
        self.chatbot = Chat(pairs, reflections)

    def get_response(self, user_input):
        return self.chatbot.respond(user_input)

# Create Streamlit app
def main():
    # Set the title of the app
    st.title("Chatbot Pétrophysicien")

    # Create a Chatbot instance
    chatbot = Chatbot(pairs, reflections)

    # Create an input box for the user to type
    user_input = st.text_input("Posez votre question:")

    if user_input:
        response = chatbot.get_response(user_input)
        st.write(f"Réponse: {response}")

if __name__ == "__main__":
    main()