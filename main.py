from utils import get_data, get_filtered_data, get_last_values, get_formatted_data


def main():
    operations_url = "https://file.notion.so/f/s/d22c7143-d55e-4f1d-aa98-e9b15e5e5efc/operations.json?spaceId=0771f0bb-b4cb-4a14-bc05-94cbd33fc70d&table=block&id=f11058ed-10ad-42ea-a13d-aad1945e5421&expirationTimestamp=1676184889687&signature=dAVoVOtHp3aozkUuyDMZEJNskPhMc2aKCKXVi6jXLno&downloadName=operations.json"
    filtered_empty_from = True
    count_last_values = 5

    data, info = get_data(operations_url)
    if not data:
        exit(info)
    else:
        print(info)

    data = get_filtered_data(data, filtered_empty_from=filtered_empty_from)
    data = get_last_values(data, count_last_values)
    data = get_formatted_data(data)

    print("INFO: Вывод данных:")
    for row in data:
        print(row, end='\n\n')

if __name__ == "__main__":
    main()

