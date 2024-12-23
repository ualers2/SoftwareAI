

def pegar_hora():
     import datetime
     current_datetime = datetime.datetime.now()
     formatted_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
     return f"{formatted_datetime}"

                