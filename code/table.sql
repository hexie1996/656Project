create table `user`(
userID varchar(50) primary key,
nickname varchar(100),
gender varchar(2),
birthday varchar(20),
bio varchar(140),
religion varchar(50)
);
create table `peopleGroup`(
groupID varchar(50) primary key,
groupName varchar(50),
peopleNum int
);
create table `topic`(
topicID varchar(50) primary key,
topicName varchar(100),
parentTopicID varchar(50)
);
create table `post`(
postID varchar(50) primary key,
userID varchar(50),
content varchar(5100),
url varchar(200),
imageUrl varchar(200),
post_time varchar(100)
);
create table statusTable(
userID varchar(50),
postID varchar(50),
likeType bool,
likeTime varchar(50),
seen bool,
seenTime varchar(50),
primary key(userID,postID)
);
create table friendsTable(
followerID varchar(50),
followingID varchar(50),
followTime varchar(50),
primary key(followerID,followingID)
);
create table userGroupTable(
groupID varchar(50),
userID varchar(50),
primary key(groupID,userID)
);
create table userTopicTable(
topicID varchar(50),
userID varchar(50),
primary key(topicID,userID)
);
create table postTopicTable(
topicID varchar(50),
postID varchar(50),
primary key(topicID,postID)
);
alter table post
add foreign key(userID) references user(userID);
alter table statusTable 
add foreign key(userID) references user(userID),
add foreign key(postID) references post(postID);
alter table friendsTable 
add foreign key(followerID) references user(userID),
add foreign key(followingID) references user(userID);
alter table userGroupTable
add foreign key(groupID) references peopleGroup(groupID),
add foreign key(userID) references user(userID);
alter table userTopicTable
add foreign key(topicID) references topic(topicID),
add foreign key(userID) references user(userID);
alter table postTopicTable
add foreign key(topicID) references topic(topicID),
add foreign key(postID) references post(postID);