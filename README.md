# 📝 Notes Tracker

A simple yet powerful application for managing notes and categories, built with Django and Django REST Framework. This project emphasizes best practices in API development and testing using pytest, factory-boy, and Faker.

## 🛠️ Technologies Used

- **Django**: Web framework for building robust web applications.
- **Django REST Framework**: Extension for Django to create RESTful APIs.
- **pytest**: Framework for writing simple and scalable test cases.
- **factory-boy**: A flexible and easy-to-use library for creating test objects.
- **Faker**: Library for generating realistic fake data for testing.

## ⚙️ Installation

To install the project dependencies, run the following command:

```bash
pip install -r requirements.txt
```

## 🏃 Running Tests

To run the tests and check the coverage, execute:

```bash
pytest --cov=tests/
```

This command will execute all the tests located in the `tests/` directory and generate a coverage report.

## ✨ Features

- Create, read, update, and delete notes and categories.
- User authentication for securing note management.
- Extensive automated testing to ensure application stability.
- RESTful API endpoints for seamless integration with front-end applications.

## 🤝 Contributing

We welcome contributions to improve the NotesAPP! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b YourNewFeature`).
3. Make your changes and commit them (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin YourNewFeature`).
5. Open a pull request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
