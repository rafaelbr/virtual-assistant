from services.watson_assistant import AssistantService
from executors.actions import ActionExecutor
import json

assistant = AssistantService()
executor = ActionExecutor()

context = {
    'timezone': 'America/Sao_Paulo'
}

userinput = ''

while True:
    result = assistant.message(userinput, context)
    context = result['context']
    if 'actions' in result:
        action = result['actions'][0]
        data = executor.executeAction(action['name'], action['parameters'])
        context[action['result_variable']] = data
        result = assistant.message('', context)
        context = result['context']
    #print(result)
    #convert /n into line break
    text = result['output']['text'][0].replace('\\n','\n')
    print(text)

    exit = False
    for intent in result['intents']:
        if intent['intent'] == 'finalizacao':
            exit = True
            break

    if exit:
        break

    userinput = input('>> ')
