# 🤝 Contributing to Hospital & Stream Bot

First off, thank you for considering contributing to this project! It’s people like you who make the Discord community such a great place.

To maintain the quality of the code and ensure a smooth development process, please follow these guidelines.

---

## 🛠️ How Can I Contribute?

### 🐛 Reporting Bugs
* Check the **Issues** tab to see if the bug has already been reported.
* If not, open a new issue. Clearly describe the problem, including steps to reproduce it and your environment details (Python version, Discord.py version).

### ✨ Suggesting Enhancements
* We are always open to new ideas for RP features or UI improvements!
* Open an issue with the tag `enhancement` and describe the feature in detail.

### 💻 Code Contributions
1. **Fork** the repository and create your branch from `main`.
2. **Setup** your development environment (don't forget the `.env` file).
3. If you've added code that should be tested, add tests.
4. Ensure your code follows **PEP 8** style guidelines.
5. **Pull Request (PR)**: Submit a PR with a clear description of what you changed.

---

## 🏗️ Development Guidelines

### 🎨 UI/UX Standards (Layout v2)
Since this bot focuses on a premium experience, all new UI components must:
* Use `ui.Container` for grouped elements.
* Follow the color scheme (e.g., `0x6441a5` for streaming, `0x2ecc71` for medical).
* Ensure all interactions are handled asynchronously (`async/await`).

### 📜 Logging Requirements
If you are developing a new module (like the Ticket system):
* Implement mandatory file logging.
* Use `discord.utils.utcnow()` for timestamps to ensure global consistency.

---

## 🚀 Commit Message Format

We prefer clean and descriptive commit messages. Please follow this format:
* `feat:` for a new feature.
* `fix:` for a bug fix.
* `docs:` for documentation changes.
* `refactor:` for code changes that neither fix a bug nor add a feature.

Example: `feat: add transcript logging for ticketing system`

---

## ⚖️ Code of Conduct
By participating in this project, you agree to abide by our simple rules:
* Be respectful to other contributors.
* No spam or irrelevant PRs.
* Help each other grow!

**Questions?** Reach out to the maintainers or open a discussion!
