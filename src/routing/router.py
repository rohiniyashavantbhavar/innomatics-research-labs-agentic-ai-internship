def route_decision(state):
    if state.get('confidence', 0) < 0.7 or not state.get('retrieved_docs'):
        return 'hitl'
    return 'auto'
