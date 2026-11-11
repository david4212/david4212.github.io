"""English: matching questions (4 pairs + 1 extra option, NMT style)."""
from matching_lib import q, write

T = {}

T["01"] = [
    q(1, "Match the sentences (1–4) with the tenses (A–E).", "Sentence", "Tense", [
        ("She reads a newspaper every day.", "Present Simple"),
        ("She is reading a newspaper now.", "Present Continuous"),
        ("She has already read today's newspaper.", "Present Perfect"),
        ("She read the newspaper yesterday.", "Past Simple")], "Future Simple"),
    q(1, "Match the time expressions (1–4) with the tenses they are typically used with (A–E).", "Time expression", "Tense", [
        ("every morning", "Present Simple"), ("at the moment", "Present Continuous"),
        ("two days ago", "Past Simple"), ("by the time she arrived", "Past Perfect")], "Future Continuous"),
    q(2, "Match the beginnings (1–4) with the endings (A–E).", "Beginning", "Ending", [
        ("By the time we arrived at the cinema,", "the film had already started."),
        ("While I was cooking dinner,", "the phone rang."),
        ("I have known Andrii", "for ten years."),
        ("This time tomorrow", "I will be flying to Rome.")], "since ten years."),
    q(2, "Match the verbs (1–4) with their past participles (A–E).", "Verb", "Past participle", [
        ("go", "gone"), ("write", "written"), ("bring", "brought"), ("choose", "chosen")], "brang"),
    q(2, "Match the sentences (1–4) with the correct verb forms (A–E).", "Sentence", "Verb form", [
        ("Look! It ___ (rain).", "is raining"),
        ("Water ___ (boil) at 100 °C.", "boils"),
        ("I ___ (never / be) to Japan.", "have never been"),
        ("When I came home, my parents ___ (already / eat).", "had already eaten")], "was raining",
      "Look! — дія зараз; загальна істина — Present Simple; досвід — Present Perfect; дія до іншої в минулому — Past Perfect."),
    q(3, "Match the sentences (1–4) with the tenses (A–E).", "Sentence", "Tense", [
        ("By next June she will have graduated.", "Future Perfect"),
        ("He had been waiting for two hours when the bus finally came.", "Past Perfect Continuous"),
        ("They have been arguing all morning.", "Present Perfect Continuous"),
        ("I was going to call you, but I forgot.", "Future in the Past"),
    ], "Future Continuous"),
    q(3, "Match the sentences (1–4) with the meanings of the verb forms (A–E).", "Sentence", "Meaning", [
        ("I'm meeting Tom at six tonight.", "a fixed personal arrangement"),
        ("The train leaves at 7:15.", "an event on a timetable"),
        ("You're always losing your keys!", "an annoying repeated habit"),
        ("Don't worry, I'll carry that bag for you.", "a decision made at the moment of speaking")],
      "a completed action in the past"),
    q(3, "Match the sentences (1–4) with the meanings of the verbs in them (A–E).", "Sentence", "Meaning", [
        ("I think she's right.", "to have an opinion"),
        ("I'm thinking about moving abroad.", "to consider a possibility"),
        ("This soup tastes too salty.", "to have a particular flavour"),
        ("The chef is tasting the soup.", "to try food to check its flavour")], "to own something",
      "Стативні дієслова (think = вважати, taste = мати смак) не вживаються в Continuous; у динамічному значенні — вживаються."),
]

T["02"] = [
    q(1, "Match the active sentences (1–4) with their passive forms (A–E).", "Active", "Passive", [
        ("They built the bridge in 1990.", "The bridge was built in 1990."),
        ("People speak English here.", "English is spoken here."),
        ("Someone has stolen my bike.", "My bike has been stolen."),
        ("They will finish the project soon.", "The project will be finished soon.")], "The bridge has built in 1990."),
    q(1, "Match the types of conditionals (1–4) with the examples (A–E).", "Type", "Example", [
        ("Zero conditional", "If you heat ice, it melts."),
        ("First conditional", "If it rains, we will stay at home."),
        ("Second conditional", "If I had a car, I would drive to work."),
        ("Third conditional", "If she had studied, she would have passed.")], "If I will see him, I tell him."),
    q(2, "Match the beginnings (1–4) with the endings (A–E).", "Beginning", "Ending", [
        ("If I were you,", "I would apologise to her."),
        ("Unless you hurry,", "you will miss the bus."),
        ("If they had left earlier,", "they wouldn't have missed the flight."),
        ("If you mix red and blue,", "you get purple.")], "you would have got purple yesterday."),
    q(2, "Match the sentences (1–4) with the correct passive forms (A–E).", "Sentence", "Verb form", [
        ("The letter ___ (send) yesterday.", "was sent"),
        ("The room ___ (clean) every day.", "is cleaned"),
        ("The road ___ (repair) at the moment.", "is being repaired"),
        ("The results ___ (announce) next week.", "will be announced")], "had been sending"),
    q(2, "Match the sentences (1–4) with their meanings (A–E).", "Sentence", "Meaning", [
        ("I wish I had more free time.", "regret about the present"),
        ("I wish I had studied harder.", "regret about the past"),
        ("If only it would stop raining!", "wanting an annoying situation to change"),
        ("I'd rather you didn't smoke here.", "a preference about another person's action")],
      "a real possibility in the future"),
    q(3, "Match the sentences (1–4) with their meanings (A–E).", "Sentence", "Meaning", [
        ("I had my hair cut yesterday.", "a hairdresser cut my hair for me"),
        ("I cut my hair yesterday.", "I cut my hair myself"),
        ("I'm having my car repaired.", "a mechanic is repairing my car by arrangement"),
        ("She had her phone stolen on the bus.", "something unpleasant happened to her")], "she stole someone's phone"),
    q(3, "Match the sentences (1–4) with the structures used in them (A–E).", "Sentence", "Structure", [
        ("If I had taken that job, I would be rich now.", "mixed conditional: past condition, present result"),
        ("If I weren't so shy, I would have spoken to her at the party.", "mixed conditional: present condition, past result"),
        ("Had I known about the problem, I would have helped.", "inverted third conditional"),
        ("Should you need any help, call me.", "inverted first conditional")], "zero conditional"),
    q(3, "Match the sentences (1–4) with the sentences that have the same meaning (A–E).", "Sentence", "Same meaning", [
        ("It is said that he is very rich.", "He is said to be very rich."),
        ("It is believed that they left yesterday.", "They are believed to have left yesterday."),
        ("It is known that she is working abroad.", "She is known to be working abroad."),
        ("It was reported that the minister had resigned.", "The minister was reported to have resigned.")],
      "He is said being very rich.", "Дія одночасна — to be / to be doing; дія раніше — to have done."),
]

T["03"] = [
    q(1, "Match the nouns (1–4) with their plural forms (A–E).", "Noun", "Plural", [
        ("child", "children"), ("mouse", "mice"), ("tooth", "teeth"), ("sheep", "sheep")], "childs"),
    q(1, "Match the phrases (1–4) with the correct prepositions (A–E).", "Phrase", "Preposition", [
        ("___ Monday", "on"), ("___ July", "in"), ("___ midnight", "at"), ("___ 2010 ___ 2015", "from … to")], "since"),
    q(2, "Match the sentences (1–4) with the correct articles (A–D).", "Sentence", "Article", [
        ("She is ___ honest woman.", "an"),
        ("___ Nile is the longest river in Africa.", "the"),
        ("I play ___ tennis on Saturdays.", "— (no article)"),
        ("He is ___ university student.", "a")],
      None, "honest починається з голосного звука; назви річок — з the; види спорту — без артикля; university починається зі звука [j]."),
    q(2, "Match the sentences (1–4) with the correct words (A–E).", "Sentence", "Word", [
        ("This book is ___, not yours.", "mine"),
        ("They really enjoyed ___ at the party.", "themselves"),
        ("___ of the two answers is correct — both are wrong.", "Neither"),
        ("Is there ___ milk left in the fridge?", "any")], "myself"),
    q(2, "Match the sentences (1–4) with the correct quantifiers (A–E).", "Sentence", "Quantifier", [
        ("How ___ money do you have?", "much"),
        ("How ___ books did you buy?", "many"),
        ("There are very ___ people here — the hall is almost empty.", "few"),
        ("We have very ___ time, so let's hurry.", "little")], "a lot of",
      "much/little — з незлічуваними, many/few — зі злічуваними; few і little без a мають значення «майже немає»."),
    q(3, "Match the sentences (1–4) with the correct prepositions (A–E).", "Sentence", "Preposition", [
        ("She is very good ___ maths.", "at"), ("He is interested ___ history.", "in"),
        ("I'm afraid ___ spiders.", "of"), ("It depends ___ the weather.", "on")], "for"),
    q(3, "Match the sentences (1–4) with the correct relative words (A–E).", "Sentence", "Relative word", [
        ("The man ___ car was stolen called the police.", "whose"),
        ("This is the house ___ I grew up.", "where"),
        ("The girl ___ you met yesterday is my sister.", "whom"),
        ("That's the reason ___ I left early.", "why")], "which"),
    q(3, "Match the phrases (1–4) with their meanings (A–E).", "Phrase", "Meaning", [
        ("in time", "early enough, before it is too late"),
        ("on time", "at exactly the planned time"),
        ("at the end", "at the final point of something"),
        ("in the end", "finally, after a long process")], "occasionally"),
]

T["04"] = [
    q(1, "Match the words (1–4) with their definitions (A–E).", "Word", "Definition", [
        ("niece", "the daughter of your brother or sister"),
        ("nephew", "the son of your brother or sister"),
        ("stepfather", "your mother's husband who is not your father"),
        ("in-laws", "the parents and relatives of your husband or wife")], "the brother of your mother or father"),
    q(1, "Match the situations (1–4) with what people say (A–E).", "Situation", "Phrase", [
        ("You meet someone for the first time.", "Nice to meet you."),
        ("Someone sneezes.", "Bless you!"),
        ("You didn't hear what someone said.", "Sorry, could you repeat that?"),
        ("Someone thanks you for your help.", "You're welcome.")], "Congratulations!"),
    q(2, "Match the phrasal verbs (1–4) with their meanings (A–E).", "Phrasal verb", "Meaning", [
        ("bring up", "to raise a child"), ("get on with", "to have a good relationship with"),
        ("look after", "to take care of"), ("take after", "to look or behave like an older relative")],
      "to end a romantic relationship"),
    q(2, "Match the verbs (1–4) with the words they go with (A–E).", "Verb", "Collocation", [
        ("do", "the washing-up"), ("make", "the bed"), ("take out", "the rubbish"), ("set", "the table")], "a shower"),
    q(2, "Match the adjectives (1–4) with the descriptions (A–E).", "Adjective", "Description", [
        ("generous", "happy to give money, time or presents"),
        ("stubborn", "refusing to change their opinion"),
        ("reliable", "always doing what they promised"),
        ("sociable", "enjoying meeting and talking to people")], "nervous and uncomfortable with other people"),
    q(3, "Match the idioms (1–4) with their meanings (A–E).", "Idiom", "Meaning", [
        ("the black sheep of the family", "a family member others are ashamed of"),
        ("like two peas in a pod", "very similar to each other"),
        ("to tie the knot", "to get married"),
        ("to run in the family", "to be common among relatives")], "to argue all the time"),
    q(3, "Match the notices (1–4) with their meanings (A–E).", "Notice", "Meaning", [
        ("OUT OF ORDER", "The machine is not working."),
        ("KEEP OFF THE GRASS", "Do not walk on the lawn."),
        ("MIND THE GAP", "Be careful when getting on or off the train."),
        ("FULLY BOOKED", "There are no free rooms or tables.")], "The shop is closed for lunch."),
    q(3, "Match the words (1–4) with their definitions (A–E).", "Word", "Definition", [
        ("spouse", "a husband or wife"), ("sibling", "a brother or sister"),
        ("fiancé", "a man who is engaged to be married"), ("widow", "a woman whose husband has died")],
      "a child whose parents have died"),
]

T["05"] = [
    q(1, "Match the words (1–4) with their definitions (A–E).", "Word", "Definition", [
        ("salary", "a fixed amount of money paid for work every month"),
        ("tuition fee", "money you pay to be taught at a college or university"),
        ("deadline", "the latest time by which something must be done"),
        ("colleague", "a person you work with")], "a person who is learning a trade from a skilled worker"),
    q(1, "Match the jobs (1–4) with their descriptions (A–E).", "Job", "Description", [
        ("surgeon", "performs medical operations"), ("accountant", "keeps and checks financial records"),
        ("plumber", "repairs water pipes and taps"), ("architect", "designs buildings")], "defends people in court"),
    q(2, "Match the verbs (1–4) with the words they go with (A–E).", "Verb", "Collocation", [
        ("apply", "for a job"), ("pass", "an exam"), ("earn", "a living"), ("chair", "a meeting")], "homework"),
    q(2, "Match the phrasal verbs (1–4) with their meanings (A–E).", "Phrasal verb", "Meaning", [
        ("drop out", "to leave school or university before finishing"),
        ("fill in", "to complete a form"),
        ("take on", "to employ someone"),
        ("lay off", "to dismiss workers because there is not enough work")], "to get a higher position at work"),
    q(2, "Match the words (1–4) with their definitions (A–E).", "Word", "Definition", [
        ("unemployment", "the state of not having a job"),
        ("poverty", "the state of being extremely poor"),
        ("discrimination", "unfair treatment of people because of their race, sex or age"),
        ("volunteering", "doing work without pay to help others")], "moving to another country to live"),
    q(3, "Match the words (1–4) with their meanings (A–E).", "Word", "Meaning", [
        ("employer", "a person or company that gives people work"),
        ("employee", "a person who is paid to work for someone"),
        ("unemployed", "without a paid job"),
        ("employment", "the state of having paid work")], "a person who trains new workers"),
    q(3, "Match the words (1–4) with their definitions (A–E).", "Word", "Definition", [
        ("undergraduate", "a student studying for a first degree"),
        ("postgraduate", "a student studying after receiving a first degree"),
        ("scholarship", "money given to a student to pay for their studies"),
        ("dissertation", "a long piece of writing done for a university degree")], "the head of a university"),
    q(3, "Match the idioms (1–4) with their meanings (A–E).", "Idiom", "Meaning", [
        ("to climb the career ladder", "to get promoted step by step"),
        ("to burn the midnight oil", "to work or study late at night"),
        ("to be on the same page", "to understand and agree with each other"),
        ("to get the sack", "to be dismissed from your job")], "to work part-time"),
]

T["06"] = [
    q(1, "Match the words (1–4) with their definitions (A–E).", "Word", "Definition", [
        ("pollution", "damage to air, water or land caused by harmful substances"),
        ("recycling", "processing used materials so they can be used again"),
        ("drought", "a long period with little or no rain"),
        ("flood", "a large amount of water covering land that is usually dry")], "a violent storm with very strong winds"),
    q(1, "Match the words (1–4) with their definitions (A–E).", "Word", "Definition", [
        ("luggage", "the bags you take with you on a journey"),
        ("departure", "the act of leaving at the start of a journey"),
        ("boarding pass", "a card that allows you to get on a plane"),
        ("souvenir", "a thing you buy to remember a place you visited")], "a document that allows you to enter a country"),
    q(2, "Match the notices (1–4) with their meanings (A–E).", "Notice", "Meaning", [
        ("GATE CLOSES 20 MINUTES BEFORE DEPARTURE", "Passengers must reach the gate in good time."),
        ("NO CAMPING", "You cannot put up a tent here."),
        ("PLEASE DO NOT FEED THE ANIMALS", "Visitors must not give food to the animals."),
        ("BOTTLES AND CANS ONLY", "This bin is only for drink containers.")], "You must buy a ticket in advance."),
    q(2, "Match the phrasal verbs (1–4) with their meanings (A–E).", "Phrasal verb", "Meaning", [
        ("set off", "to start a journey"), ("check in", "to register at a hotel or airport"),
        ("get away", "to go somewhere for a holiday or rest"), ("look around", "to explore a place")],
      "to return home"),
    q(2, "Match the terms (1–4) with their definitions (A–E).", "Term", "Definition", [
        ("endangered species", "animals or plants that may soon disappear"),
        ("habitat", "the natural home of an animal or plant"),
        ("deforestation", "cutting down large areas of forest"),
        ("global warming", "a rise in the average temperature of the Earth")], "animals that hunt other animals"),
    q(3, "Match the words (1–4) with the words they go with (A–E).", "Word", "Collocation", [
        ("carbon", "footprint"), ("renewable", "energy"), ("greenhouse", "effect"), ("acid", "rain")], "species"),
    q(3, "Match the idioms (1–4) with their meanings (A–E).", "Idiom", "Meaning", [
        ("off the beaten track", "in a quiet place that few tourists visit"),
        ("to hit the road", "to start a journey"),
        ("to travel light", "to travel with very little luggage"),
        ("a tourist trap", "a place that charges tourists too much")], "to miss a flight"),
    q(3, "Match the words (1–4) with their definitions (A–E).", "Word", "Definition", [
        ("journey", "the act of travelling from one place to another"),
        ("trip", "a short visit to a place and back, often for pleasure"),
        ("voyage", "a long journey by sea or in space"),
        ("excursion", "a short organised trip, often as part of a holiday")], "the area where you live"),
]

H = "Read the texts (1–4) and match them with the headings (A–E). One heading is extra."
T["07"] = [
    q(1, H, "Text", "Heading", [
        ("Our school opens at 8 a.m. Lessons last 45 minutes, and there is a long break at 11.", "Daily timetable"),
        ("After classes, students can join the chess club, the choir or the football team.", "After-school activities"),
        ("The canteen serves hot meals and fresh salads at low prices.", "School meals"),
        ("Every May we organise a trip to the Carpathians for all classes.", "Annual excursion")], "Exam results"),
    q(1, H, "Text", "Heading", [
        ("Doctors recommend that teenagers sleep at least eight hours a night.", "Rest well"),
        ("Fresh fruit and vegetables should make up half of your plate.", "Eat smart"),
        ("Just thirty minutes of walking a day can make your heart stronger.", "Keep moving"),
        ("Drinking enough water helps you concentrate and prevents headaches.", "Stay hydrated")], "Visit your dentist"),
    q(2, H, "Text", "Heading", [
        ("Admission is free for children under seven. Students pay half price with a valid card.", "Ticket prices"),
        ("Large bags and umbrellas must be left in the cloakroom on the ground floor.", "Before you go in"),
        ("You may take photos, but flash can damage old paintings and is not allowed.", "Taking pictures"),
        ("Guided tours in English start every hour from the main hall.", "Explore with an expert")], "Opening hours"),
    q(2, H, "Text", "Heading", [
        ("Last summer Olena spent two weeks cleaning a beach near Odesa with other students.", "Helping nature"),
        ("Ivan, a retired teacher, gives free maths lessons to children from his village.", "Sharing knowledge"),
        ("Every Saturday a group of students cooks hot meals for homeless people.", "Feeding those in need"),
        ("Many volunteers say the experience helped them choose their future careers.", "An unexpected benefit")],
      "Well-paid summer jobs"),
    q(2, H, "Text", "Heading", [
        ("Smartphones let us read the news, pay for shopping and talk to friends from anywhere.", "Everything in your pocket"),
        ("However, scientists warn that the blue light from screens can disturb our sleep.", "A hidden danger at night"),
        ("Some families now have 'phone-free dinners' so that they can talk face to face.", "Disconnecting together"),
        ("Experts expect that in ten years most devices will be controlled by voice.", "Looking ahead")],
      "The history of the telephone"),
    q(3, H, "Text", "Heading", [
        ("When the first tourists came, the village had no hotel, so local families opened their homes to guests.", "Hospitality born of necessity"),
        ("Within ten years the quiet fishing port had become a busy resort with traffic jams every weekend.", "A rapid transformation"),
        ("Older residents complain that they hardly recognise the place where they grew up.", "Missing the old days"),
        ("The council has now limited new construction to protect the coastline.", "Taking control of growth")],
      "Fishing is still the main industry", "Зайвий заголовок суперечить тексту 2: селище перетворилося на курорт."),
    q(3, H, "Text", "Heading", [
        ("Bees pollinate about a third of the crops that end up on our plates.", "Why bees matter"),
        ("Yet the number of bees has fallen sharply because of pesticides and the loss of wild flowers.", "A worrying decline"),
        ("In several European cities, residents now keep hives on the roofs of their buildings.", "Beekeeping in the city"),
        ("Researchers are even testing tiny drones that could pollinate plants if bees disappear.", "A high-tech plan B")],
      "How honey is made"),
    q(3, H, "Text", "Heading", [
        ("At first Mark thought working from home would be a dream: no traffic and no dress code.", "High expectations"),
        ("But after a month he realised that he hardly spoke to anyone all day.", "The loneliness problem"),
        ("So he started going to a co-working space twice a week just to be among people.", "Finding a balance"),
        ("Now he says the secret is not where you work, but how you organise your day.", "The real lesson")],
      "Asking for a pay rise"),
]

FILES = {
    "01": "01_grammar_tenses", "02": "02_grammar_passive", "03": "03_grammar_nouns",
    "04": "04_vocabulary_everyday", "05": "05_vocabulary_education", "06": "06_vocabulary_environment",
    "07": "07_reading",
}

if __name__ == "__main__":
    for k, qs in T.items():
        write("english", FILES[k], FILES[k] + "_match.json", qs)
