def fb_parsing(access_token, chat_id, page):
    graph = fb.GraphAPI(access_token)
    profile = graph.get_object(page)
    posts = graph.get_connections(id=profile['id'], connection_name='feed')['data']
    months = {'января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября',
              'декабря'}
    monthsOrder = {'января': 1, 'февраля': 2, 'марта': 3, 'апреля': 4, 'мая': 5, 'июня': 6,  #
                   'июля': 7, 'августа': 8, 'сентября': 9, 'октября': 10, 'ноября': 11, 'декабря': 12}
    eventsEndWordsSet = {'до', 'по'}
    futureEvents = []
    futureEvents_new = []
    try:
        futureEvents = list(pd.read_csv('futureEvents_' + str(chat_id) + '.csv').post_id)
    except:
        futureEvents = []
        file = open('futureEvents_' + str(chat_id) + '.csv', 'w')
        file.write('post_id')
        file.close()
    for post in posts:
        getStartDate = 0
        getEndDate = 0
        try:
            text = post['message']
            text = text.replace('\n', ' ')
            wordsList = text.split()
            for wordPos in range(len(wordsList)):
                wordsList[wordPos] = wordsList[wordPos].strip('.').strip(',').strip('-')
            for wordPos in range(len(wordsList)):
                if wordsList[wordPos] in months and re.match(r'[0-9][0-9]\b', wordsList[wordPos - 1]):
                    try:
                        if re.match(r'[0-9][0-9][0-9][0-9]\b', wordsList[wordPos + 1]) \
                                and wordsList[wordPos + 2] == 'года':
                            pass
                            # print(wordsList)
                    except:
                        pass

                    else:
                        eventMonth = monthsOrder[wordsList[wordPos]]
                        eventYear = datetime.now().year
                        if (eventMonth < datetime.now().month):
                            eventYear = eventYear + 1
                        eventDay = int(wordsList[wordPos - 1])
                        if getStartDate == 0:
                            getDate = 1
                            eventStart = date(eventYear, eventMonth, eventDay)
                        try:
                            if (wordsList[wordPos - 2] in eventsEndWordsSet) and getEndDate == 0:
                                getEndDate = 1
                                eventEnd = date(eventYear, eventMonth, eventDay)
                        except:
                            pass
                            # print(datetime.date(datetime.now()), eventStart)
            if (datetime.date(datetime.now()) <= eventStart):
                futureEvents_new.append(
                    dict({'id': post['id'], 'from': eventStart, 'to': eventEnd, 'main': post['message']}))
                # print(post['message'])
        except KeyError:
            pass
    pd.DataFrame(futureEvents + futureEvents_new, columns=['post_id']).to_csv('futureEvents_' + str(chat_id) + '.csv',
                                                                          index=False)