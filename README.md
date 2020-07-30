# sms
School Management System for Students and Teachers

# Project Setup

## Without docker
```
git clone .
cd sms
git checkout develp
python3 -m venv env
source env/bin/activate
pip install -r requirements/development.txt
./manane.py runserver
```

## With Docker
```
git clone .
cd sms
docker-compose up --build
```

# API end Points

## Register API
http://127.0.0.1:8000/api/v1/auth/register/

POST DATA
```
{
    "email": "ram@atlogys.com",
    "username": "ram",
    "user_type": "T",
    "first_name": "Ram",
    "last_name": "Chauhan",
    "password": "qwerty@123",
    "password2": "qwerty@123"
}
```

## Login API

http://127.0.0.1:8000/api/v1/auth/login/

POST DATA

```
{
    "email": "",
    "password": ""
}
```

As part of this api you will get a Token, you need to use that token to
communicate with other apis

## Logout API

http://127.0.0.1:8000/api/v1/auth/logout/


## Student List API

http://127.0.0.1:8000/api/v1/students/

Resposne:
```
[
    {
        "id": 1,
        "user": {
            "id": 2,
            "email": "ram+1@atlogys.com",
            "username": "ram",
            "user_type": "Student",
            "first_name": "Ram",
            "last_name": "Chauhan",
            "is_active": true
        }
    },
    {
        "id": 2,
        "user": {
            "id": 3,
            "email": "ram+2@atlogys.com",
            "username": "ram",
            "user_type": "Student",
            "first_name": "Ram",
            "last_name": "Chauhan",
            "is_active": true
        }
    },
    {
        "id": 3,
        "user": {
            "id": 4,
            "email": "ram+3@atlogys.com",
            "username": "ram",
            "user_type": "Student",
            "first_name": "Ram",
            "last_name": "Chauhan",
            "is_active": true
        }
    },
    {
        "id": 4,
        "user": {
            "id": 5,
            "email": "ram+4@atlogys.com",
            "username": "ram",
            "user_type": "Student",
            "first_name": "Ram",
            "last_name": "Chauhan",
            "is_active": true
        }
    }
]
```

## Student Detail API

http://127.0.0.1:8000/api/v1/students/1/

Resposne
```
{
    "id": 1,
    "user": {
        "id": 2,
        "email": "ram+1@atlogys.com",
        "username": "ram",
        "user_type": "S",
        "first_name": "Ram",
        "last_name": "Chauhan",
        "is_active": true
    }
}
```

## Teacher List API

http://127.0.0.1:8000/api/v1/teachers/

Response:
```
[
    {
        "id": 1,
        "user": {
            "id": 1,
            "email": "ram@atlogys.com",
            "username": "ram",
            "user_type": "Teacher",
            "first_name": "Ram",
            "last_name": "Chauhan",
            "is_active": true
        },
        "students": []
    }
]
```

## Teacher Detail API

http://127.0.0.1:8000/api/v1/teachers/1/

Response:
```
{
    "id": 1,
    "user": {
        "id": 1,
        "email": "ram@atlogys.com",
        "username": "ram",
        "user_type": "Teacher",
        "first_name": "Ram",
        "last_name": "Chauhan",
        "is_active": true
    },
    "students": [
        1
    ]
}
```

## Teacher Attach Student API

http://127.0.0.1:8000/api/v1/teachers/1/attach_students/

POST DATA:
```
{
    "students_ids": [1]
}
```
Response:
```
{
    "success": "Sucessfully Added"
}
```

## Teacher mark star Student API

http://127.0.0.1:8000/api/v1/teachers/1/rate_students/

POST DATA:
```
{
    "student_id": [1, 2]
}
```

Response:
```
{
    "success": "Marked Star Student successfully"
}
```

ValidationError:
```
{
    "non_field_errors": [
        "{2} are not valid Student IDs"
    ]
}
```

# GraphQL query

## Teachers query and star students
```
query teachers{
  teachers{
    id,
    user{
      firstName
      lastName
    }
    students{
      id
      user{
        firstName
        lastName
      }
    }
  }
}
```

## Students Query

```
query studnet{
  students{
    id
    user{
      firstName
      lastName
    }
  }
}
```

# Mark and Unmark student Star Mutation

```
mutation StudnetStar{
  	starStudent(teacherId: 1, studentIds: [1], markStar: true){
        errorMessages
        message
  }
}
```
