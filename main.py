import requests
import config
import os


def get_gelbooru():
    user_tags = input("Tags: ").replace(' ', '_')
    url = 'https://gelbooru.com/'
    api_url = f'{url}index.php?page=dapi&s=post&q=index&api_key={config.API_KEY}&user_id={config.USER_ID}&tags={user_tags}&json=1'

    response = requests.get(api_url)
    src = response.json()

    posts = src['post']

# Checking whether directory with this tag exists

    if os.path.exists(f"{user_tags}"):
        print(f"{user_tags} directory already exists!")
    else:
        os.mkdir(user_tags)

# Collecting new IDs
    new_posts_id = []

    for new_post_id in posts:
        new_post_id = new_post_id['id']
        new_posts_id.append(new_post_id)

    if not os.path.exists(f"{user_tags}/exist_posts_{user_tags}.txt"):
        print("Files with this id does not exist")

        with open(f"{user_tags}/exist_posts_{user_tags}.txt", 'w') as file:
            for id in new_posts_id:
                file.write(str(id) + "\n")

        os.mkdir(f"{user_tags}/downloads")

        for image in posts:
            download_image = requests.get(image['file_url'])
            with open(f"{user_tags}/downloads/{image['id']}.jpg", "wb") as file:
                file.write(download_image.content)

    else:
        print("Aha, this is already here!")
        pagination = 1
        api_url = f'{url}index.php?page=dapi&s=post&q=index&api_key={config.API_KEY}&user_id={config.USER_ID}&tags={user_tags}&json=1&pid={pagination}'
        response = requests.get(api_url)
        src = response.json()

        posts = src['post']

        for image in posts:
            pagination += 1
            download_image = requests.get(image['file_url']).content
            if not os.path.exists(f"{user_tags}/downloads/{image['id']}.jpg"):
                with open(f"{user_tags}/downloads/{image['id']}.jpg", "wb") as file:
                    file.write(download_image)
        else:
            print("Image with this id already exists")


def main():
    get_gelbooru()


if __name__ == '__main__':
    main()



