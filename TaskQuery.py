questions = ['What is the range of incubation periods for the disease in humans?',
'What do we know about the basic reproduction number?',
'How long are individuals are contagious?',
'What do we know about asymptomatic transmission in children?',
'What do we know about seasonality of transmission?',
'What do we know about viral shedding duration?',
'How long are individuals are contagious, even after recovery?',
'Does the range of incubation period vary across age groups?',
'Does the range of incubation period vary with children?',
'Does the range of incubation period vary based on underlying health?',
'What is the prevalance of asymptomatic transmission?']

topics = ['Range of incubation periods for the disease in humans',
'Prevalence of asymptomatic shedding and transmission',
'Seasonality of transmission',
'Physical science of the coronavirus',
'Persistence and stability on a multitude of substrates and sources',
'Persistence of virus on surfaces of different materials',
'Natural history of the virus and shedding of it from an infected person',
'Implementation of diagnostics and products to improve clinical processes',
'Disease models, including animal models for infection, disease and transmission',
'Tools and studies to monitor phenotypic change and potential adaptation of the virus',
'Immune response and immunity',
'Effectiveness of personal protective equipment',
'Role of the environment in transmission']

class TaskQuery:
    @staticmethod
    def questions():
        return questions

    @staticmethod
    def topics():
        return topics
