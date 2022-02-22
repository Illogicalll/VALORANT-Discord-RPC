from pypresence import Presence

def startRPC():
    global rpc
    rpc = Presence("945758612175851602")
    rpc.connect()

def updateRPC(variation, state, partyMembers, mapName, homeScore, awayScore, gameMode):
    if variation == 1:
        rpc.update(details=f'{homeScore} - {awayScore} | {mapName}  ({gameMode})  ', state=f'In-Party {partyMembers} of 5', large_image='logo')
    elif variation == 2:
        rpc.update(details=f'{state} : {mapName}', state=f'Party Size {partyMembers} of 5', large_image='logo')
    elif variation == 3:
        rpc.update(details=f'{state}', state=f'Party Size {partyMembers} of 5', large_image='logo')