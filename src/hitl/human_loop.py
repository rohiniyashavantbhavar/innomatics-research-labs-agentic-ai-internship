def human_intervention(state):
    print('\nEscalated to Human Support')
    state['answer'] = input('Enter human response: ')
    return state
