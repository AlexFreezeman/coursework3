import requests
from datetime import datetime


def get_data(url):
    """
    Получает данные с url, выводит ошибку на случай некорректной работы
    :param url:
    :return: response or None + info
    """
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json(), "INFO: Данные получены успешно\n"
        return None, f"ERROR: status_code:{response.status_code}\n"
    except requests.exceptions.ConnectionError:
        return None, "ERROR: requests.exceptions.ConnectionError\n"
    except requests.exceptions.JSONDecodeError:
        return None, "ERROR: requests.exceptions.JSONDecodeError\n"


def get_filtered_data(data, filtered_empty_from=False):
    """
    Фильтрует данные, убирает отмененные операции
    :param data:
    :param filtered_empty_from:
    :return: data
    """
    data = [x for x in data if "state" in x and x["state"] == "EXECUTED"]
    if filtered_empty_from:
        data = [x for x in data if "from" in x]
    return data


def get_last_values(data, count_last_values):
    """
    Сортирует по дате проведения операции, возвращает в обратном порядке
    :param data:
    :param count_last_values:
    :return: data
    """
    data = sorted(data, key=lambda x: x["date"], reverse=True)
    data = data[:count_last_values]
    return data


def get_formatted_data(data):
    """
    Форматирует данные в шаблон (см. README.md)
    :param data:
    :return: formatted_data
    """
    formatted_data = []
    for row in data:
        date = datetime.strptime(row["date"], "%Y-%m-%dT%H:%M:%S.%f").strftime("%d.%m.%Y")
        description = row["description"]
        from_info, from_bill = "", ""
        if "from" in row:
            sender = row["from"].split()
            receiver = row["to"].split()
            from_bill = sender.pop(-1)
            to_bill = receiver.pop(-1)
            if "Счет" in sender:
                from_bill = f"**{from_bill[-4:]}"
            else:
                from_bill = f"{from_bill[:4]} {from_bill[4:6]}** **** {from_bill[-4:]}"
            from_info = " ".join(sender)
            if "Счет" in receiver:
                to_bill = f"**{to_bill[-4:]}"
            else:
                to_bill = f"{to_bill[:4]} {to_bill[4:6]}** **** {to_bill[-4:]}"
            to_info = " ".join(receiver)

        operation_amount = f"{row['operationAmount']['amount']} {row['operationAmount']['currency']['name']}"

        formatted_data.append(f"""\
{date} {description}
{from_info} {from_bill} -> {to_info} {to_bill}
{operation_amount}""")

    return formatted_data
