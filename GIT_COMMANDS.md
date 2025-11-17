# Git Commands - Quick Reference

## 🚀 Complete Setup (Copy & Paste)

### 1. Initialize Git
```bash
git init
```

### 2. Add All Files
```bash
git add .
```

### 3. Check Status
```bash
git status
```

### 4. First Commit
```bash
git commit -m "Initial commit: Smart Dispatch Agent"
```

### 5. Create GitHub Repository
- Go to: https://github.com/new
- Name: `smart-dispatch-agent`
- Click "Create repository"

### 6. Connect to GitHub
```bash
git remote add origin https://github.com/YOUR_USERNAME/smart-dispatch-agent.git
```

**Replace `YOUR_USERNAME` with your actual GitHub username!**

### 7. Push to GitHub
```bash
git branch -M main
git push -u origin main
```

---

## 📋 Daily Git Commands

### Check Status
```bash
git status
```

### Add Files
```bash
git add .                    # Add all files
git add filename.py          # Add specific file
```

### Commit Changes
```bash
git commit -m "Description of changes"
```

### Push to GitHub
```bash
git push
```

### Pull from GitHub
```bash
git pull
```

### View History
```bash
git log
```

---

## 🔄 Common Workflows

### Making Changes and Pushing

```bash
# 1. Make your changes to files

# 2. Check what changed
git status

# 3. Add changed files
git add .

# 4. Commit with message
git commit -m "Added new feature: dashboard filters"

# 5. Push to GitHub
git push
```

### Creating a New Branch

```bash
# Create and switch to new branch
git checkout -b feature/new-feature

# Make changes, then:
git add .
git commit -m "New feature"
git push origin feature/new-feature
```

---

## ⚠️ Important Notes

1. **Always check `git status`** before committing
2. **Write clear commit messages**
3. **Never commit passwords** - use environment variables
4. **Pull before pushing** if working with others
5. **Use `.gitignore`** to exclude unnecessary files

---

## 🐛 Troubleshooting

### "Repository not found"
- Check repository URL
- Verify you have access
- Check GitHub username

### "Authentication failed"
- Use Personal Access Token (not password)
- GitHub → Settings → Developer settings → Personal access tokens

### "Files not showing"
- Check `.gitignore` isn't excluding them
- Use `git add -f filename` to force add

---

## 📖 Learn More

- Git Documentation: https://git-scm.com/doc
- GitHub Guides: https://guides.github.com
- Git Cheat Sheet: https://education.github.com/git-cheat-sheet-education.pdf

