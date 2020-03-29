import requests
base_url="http://127.0.0.1:5000/"
def home():
    while(1):
        print("welcome to my tiny social network, please input your user id:")
        user_id = input("User ID:")
        response = requests.get(base_url+"user?user_id="+user_id)
        if '[]' in response.text:
            print("invalid user id, please input again.")
            continue
        else:
            login(user_id)
def login(user_id):
    while(1):
        print("#################################################")
        print("please input the index of the function you need:")
        print("a.send a post")
        print("b.follow a person")
        print("c.like/dislike a post")
        print("d.follow a topic")
        print("e.follow a group")
        print("f.create a topic")
        print("g.create a group")
        print("h.see new posts of people")
        print("i.see new posts of topics")
        print("j.see new posts of groups")
        print("k.see my friend list")
        print("l.see all the posts of one person")
        print("m.see all the posts of one topic")
        print("n.see all the groups' information")
        print("o.log out")
        print("#################################################")
        choose = input("please input your choice:")
        if choose == 'a':
            send_a_post(user_id)
        elif choose == 'b':
            follow_a_person(user_id)
        elif choose == 'c':
            like(user_id)
        elif choose == 'd':
            follow_a_topic(user_id)
        elif choose == 'e':
            follow_a_group(user_id)
        elif choose == 'f':
            create_a_topic()
        elif choose == 'g':
            create_a_group()
        elif choose == 'h':
            get_friends_post(user_id)
        elif choose == 'i':
            get_topic_post(user_id)
        elif choose == 'j':
            get_group_post(user_id)
        elif choose == 'k':
            friend_list(user_id)
        elif choose == 'l':
            one_user_post()
        elif choose == 'm':
            one_topic_post()
        elif choose == 'n':
            all_groups()
        elif choose == 'o':
            break
    home()
#post functions
def send_a_post(user_id):
    content=input("please input the content:")
    topic_id=input("please input the topic id:")
    if topic_id == "":
        topic_id = "None"
    data={'content':content,'userID':user_id,'topicID':topic_id}
    print(requests.post(base_url+"send_post",json=data).text)

def follow_a_person(user_id):
    friend_id=input("please input the user's id:")
    data={'followerID':user_id,'followingID':friend_id}
    print(requests.post(base_url + "follow_person", json=data).text)

def like(user_id):
    post_id=input("please input the post's id:")
    likeType=input("like for 1, dislike for 2:")
    if likeType=='1':
        likeType='true'
    elif likeType=='2':
        likeType='false'
    else:
        print("your input is not valid")
        return
    data={'userID':user_id,'postID':post_id,'likeType':likeType}
    print(requests.post(base_url + "like", json=data).text)

def follow_a_topic(user_id):
    topic_id=input("please input the topic's id:")
    data={'userID':user_id,'topicID':topic_id}
    print(requests.post(base_url + "follow_topic", json=data).text)

def follow_a_group(user_id):
    group_id=input("please input the group's id:")
    data={'userID':user_id,'groupID':group_id}
    print(requests.post(base_url + "follow_group", json=data).text)

def create_a_topic():
    topic_name = input("please input the topic's name:")
    data = {'topicName': topic_name}
    print(requests.post(base_url + "create_topic", json=data).text)

def create_a_group():
    topic_name = input("please input the group's name:")
    data = {'groupName': topic_name}
    print(requests.post(base_url + "create_group", json=data).text)
#get functions
def get_friends_post(user_id):
    print(requests.get(base_url + "friends_post?user_id="+user_id).text)
def get_topic_post(user_id):
    print(requests.get(base_url + "topic_post?user_id="+user_id).text)
def get_group_post(user_id):
    print(requests.get(base_url + "group_post?user_id="+user_id).text)
def friend_list(user_id):
    print(requests.get(base_url + "friend_list?user_id=" + user_id).text)
def one_user_post():
    user_id=input("please input the user's id:")
    print(requests.get(base_url + "all_person?user_id=" + user_id).text)
def one_topic_post():
    topic_id=input("please input the topic's id:")
    print(requests.get(base_url + "all_topic?topic_id=" + topic_id).text)
def all_groups():
    print(requests.get(base_url + "all_group").text)

if __name__ == '__main__':
    home()
