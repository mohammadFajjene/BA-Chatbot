from statemachine import StateMachine, State

class ChatbotStates(StateMachine):

    # defining states
    greetings = State('Greeting', initial=True)
    departments = State('Departments')
    subjects = State('Subjects')
    exams = State('Exams')
    doctors = State('Doctors')
    goodbye = State('Goodbye')

    # defining transitions
    greetings_to_departments = greetings.to(departments)
    greetings_to_subjects = greetings.to(subjects)
    greetings_to_exams = greetings.to(exams)
    greetings_to_doctors = greetings.to(doctors)
    greetings_to_goodbye = greetings.to(goodbye)

    departments_to_subjects = departments.to(subjects)
    departments_to_exams = departments.to(exams)
    departments_to_doctors = departments.to(doctors)
    departments_to_goodbye = departments.to(goodbye)

    subjects_to_departments = subjects.to(departments)
    subjects_to_exams = subjects.to(exams)
    subjects_to_doctors = subjects.to(doctors)
    subjects_to_goodbye = subjects.to(goodbye)

    exams_to_departments = exams.to(departments)
    exams_to_subjects = exams.to(subjects)
    exams_to_doctors = exams.to(doctors)
    exams_to_goodbye = exams.to(goodbye)

    doctors_to_departments = doctors.to(departments)
    doctors_to_subjects = doctors.to(subjects)
    doctors_to_exams = doctors.to(exams)
    doctors_to_goodbye = doctors.to(goodbye)

