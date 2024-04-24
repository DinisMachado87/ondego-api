![Job it - Presentation image](documentation/main.png)

# öndëgö | README

## Overview

## Features

### 1. 


## How to Use

### 1. 

## Development User Stories

## Languages:

## Frameworks and Libraries

- **[Django==3.2.25](https://www.djangoproject.com/)**: Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. It includes built-in features for authentication, URL routing, template engine, and more.

- **[djangorestframework==3.15.1](https://pypi.org/project/djangorestframework/)**: Django REST Framework is a powerful and flexible toolkit for building Web APIs in Django. It provides serialization, authentication, permissions, and other utilities for creating RESTful APIs.

- **[pillow==10.3.0](https://pypi.org/project/Pillow/)**: Pillow is a Python Imaging Library (PIL) fork. It adds support for opening, manipulating, and saving many different image file formats. Pillow is commonly used for image processing tasks in Django applications.

- **[pytz==2024.1](https://pypi.org/project/pytz/)**: Pytz is a Python library that provides timezone definitions and utilities. It allows you to work with datetime objects in different timezones, facilitating timezone-aware datetime calculations and conversions.

## Additional Dependencies

- **[asgiref==3.8.1](https://pypi.org/project/asgiref/)**: ASGI (Asynchronous Server Gateway Interface) is a specification for building asynchronous Python web applications and servers. `asgiref` provides the base ASGI implementation for Python.

- **[cloudinary==1.39.1](https://pypi.org/project/cloudinary/)**: Cloudinary is an end-to-end image and video management solution for web and mobile applications. It offers cloud-based storage, image manipulation, optimization, and delivery.

- **[django-cloudinary-storage==0.3.0](https://pypi.org/project/django-cloudinary-storage/)**: Django Cloudinary Storage is a Django storage backend for Cloudinary, allowing you to seamlessly integrate Cloudinary with your Django application for file storage and retrieval.

- **[sqlparse==0.4.4](https://pypi.org/project/sqlparse/)**: SQLParse is a non-validating SQL parser for Python. It provides functions to parse SQL statements and SQL-like syntax.

### Other tools:

[VSCode:](https://code.visualstudio.com/) was used as the main tool to write and edit code.

[GitHub:](https://github.com/) was used to host the code of the website.

[Heroku:](https://id.heroku.com/login) Utilized for deployment and hosting of the web application, providing a scalable platform with integrated continuous delivery and deployment features.

[ElephantSQL: ](https://www.elephantsql.com/) Employed as the PostgreSQL database hosting service, offering a managed cloud database solution for storing and managing application data efficiently.

## Functionality

###  Functionality 1


## Deployment

## Manual Testing

## Resolved bugs

### Implementing Friends App
 The journey to implementing the "Friends" feature to a working solution was not straightforward.

#### Initial Approach
Initially, I implemented a Friend model with a befriended field, which represented the user to be befriended. I also added logic in the serializer through a serializer method field that created friend, requested and request method fields checking if one of both users had the other as befriended, as well as requested and requesting profiles.

However, this approach led to several issues. One of the main problems was that it was not possible to use serializer method fields as parameters for DjangoFilterBackend. This limitation led to bugs and complications in my codebase.

#### Learning from Mistakes
These bugs highlighted the importance of defining these methods inside the Friend app and the significance of modularity in Django REST Framework. By adhering to good practices, I could ensure the maintainability of my code.

My primary debugging focus was to find a solution for verifying that both users approved the friendship through a field in the Friends app. This field, initially called befriended, was checked before the creation of the Friend instance. The challenge was to achieve this without overcomplicating the code.

#### Mid-version Iteration
In an intermediate version of the application, I attempted to move the creation of the method fields to the Profile serializer. This move was intended to make these fields accessible as filters to create views in the Profiles views app.

I tried to have serializer classes create the FriendRequest, FriendsRequested, and FriendId fields there too. These fields checked if one or both users had the other as a befriended field in the Friends app.

#### Final Implementation
In the final version, I implemented a FriendRequest model, which acts as an intermediary between two users to request friendship. I also added a Friend model to represent a user's friend.

I used Django signals to handle the creation and deletion of Friend instances. When a FriendRequest was approved, Friend instances were created for both users. When a Friend instance was deleted, the corresponding Friend instance was also deleted.

This approach provided a clean, modular solution that adhered to Django REST Framework's good practices. It allowed me to maintain a manageable codebase and provided a robust solution for the "Friends" feature.

In conclusion, it showed me the importance of modularity, good practices, and careful debugging.

#### Permissions

I encountered an issue where the user receiving the request could not approve or reject the friend request and realized it was due to the IsOwnerOrReadOnly permission class often used in Django REST Framework. This permission class only allows the owner of the object to edit it, which was not the case for friend requests.

To resolve this issue, I created a custom permission class called IsFriendRequestedOrReadOnly. This permission class checks if the user is the recipient of the friend request and allows them to approve or reject it. It still allows both the sender and recipient to delete the friend request, so that the sender can cancel the request if they wish.


### Debugging the Friend Requests

I encountered an issue where I couldn't create friend requests in the API. Since most of the fields are part of an automated process and not manually edited, troubleshooting this problem was crucial. Upon investigation, I identified the root cause: the form was not rendering due to a misconfiguration in the serializer.

The only manually editable field, `to_user`, which defines the user being friend-requested, was mistakenly marked as read-only in the serializer. As a result, the form was rendered without any fields, preventing users from creating friend requests.

To resolve this issue, I updated the serializer to make the `to_user` field writable. By correcting this misconfiguration, users are now able to create friend requests successfully through the API.

### Recursive Deletion

The first issue was a recursive deletion when a `Friend` instance was deleted. In the `handle_friend_deletion` signal handler, I was trying to find and delete the corresponding `Friend` instance. However, deleting this corresponding `Friend` instance would trigger the `handle_friend_deletion` signal again, leading to a recursive loop.

To solve this, I disconnected the signal before deleting the corresponding `Friend` instance and then reconnected it afterwards. This ensured that the deletion of the corresponding `Friend` instance wouldn't trigger the signal again.

### Duplicate Friend Requests

The second issue was that our `FriendRequest` model allowed a user to send multiple friend requests to the same user. This was because there was no constraint that prevented a user from sending a friend request to a user they'd already sent a request to.

To prevent this, I added a unique constraint on the `owner` and `to_user` fields in the `FriendRequest` model. This ensured that a user could only have one outgoing friend request to another user at a time.

### Mutual Friend Requests

The third issue was that a user could create a friend request to a user who had already sent them a friend request which was causing serious issues in the handling of the friend requests in the front end as well as the conditional rendering of the buttons for it. 

To solve this, I added a check in the `save` method of the `FriendRequest` model. Before saving a `FriendRequest` instance, I checked if there was already a `FriendRequest` instance from the other user. If such a `FriendRequest` instance existed, I raised a `ValidationError`. This prevented a user from creating a friend request if there was already an existing friend request from the other user.

### Friend Request Approval

The fourth issue was that the friend request approval process was not working as expected. When a user approved a friend request the non-reversed friend request validation was not allowing the friend request to be approved. 

To solve this, I changed the validation in the `FriendRequest` to allow PUT requests but not POST requests.

## Contributors

Dinis Machado

## Credits

All emojis designed by OpenMoji – the open-source emoji and icon project. License: CC BY-SA 4.0

## Resources

[React-Bootstrap5 documentation]()

[Django Rest Framework documentation](https://www.django-rest-framework.org/)

Code Institute React and Rest Framework Walkthrough Tutorial Projects - access restricted to students

## Acknowledgments

A special thank you to the oversight and discussion insight from my Code Institute mentor Juliia Konn

## Verification

