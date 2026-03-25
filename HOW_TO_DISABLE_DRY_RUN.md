# 🔓 How to Disable DRY_RUN Mode

## Current Status

**DRY_RUN is ENABLED** (Line 15 in .env file)

```bash
DRY_RUN=true
```

This means:
- ✅ All code runs normally
- ✅ Files are detected and processed
- ✅ Logs are written
- ❌ No real emails sent
- ❌ No real payments made
- ❌ No real API calls

---

## 🚀 To Enable Real Actions

### Option 1: Edit .env File Manually

**Open .env in any text editor:**
```bash
notepad .env
```

**Change line 15 from:**
```bash
DRY_RUN=true
```

**To:**
```bash
DRY_RUN=false
```

**Save and close.**

---

### Option 2: Use Command Line

```bash
# Windows
cd "C:\Users\computer lab\Documents\GitHub\hackathon_0"
(Get-Content .env) -replace 'DRY_RUN=true', 'DRY_RUN=false' | Set-Content .env

# Or use sed (if available)
sed -i 's/DRY_RUN=true/DRY_RUN=false/' .env
```

---

## ⚠️ IMPORTANT: Before Disabling

### You MUST Have These Setup:

**1. Gmail API Credentials (if using Gmail watcher)**
- [ ] credentials.json file downloaded from Google Cloud Console
- [ ] OAuth token created (happens on first run)

**2. WhatsApp Login (if using WhatsApp watcher)**
- [ ] WhatsApp Web session saved in .whatsapp_session/

**3. Test Everything First**
- [ ] Run `python test_system.py` - all tests pass
- [ ] Run `python demo.py` - demo works
- [ ] Verify approval workflow

---

## 🎯 Recommendation for Hackathon

### KEEP DRY_RUN=true ✅

**Why?**
1. ✅ **Safe to demo** - No accidental actions
2. ✅ **Works without credentials** - No setup needed
3. ✅ **Judges can test** - Safe for everyone
4. ✅ **Proves concept** - Shows system works
5. ✅ **Professional** - Production safety feature

**In your video:**
```
"The system is in DRY_RUN mode for safe testing. This is a
production best practice that prevents accidental actions
during development and demos. It can be disabled when
credentials are configured and the system is ready for
production use."
```

---

## 🔄 What Changes When You Disable

### With DRY_RUN=false:

**Email MCP will:**
- ✅ Actually send emails via Gmail API
- ⚠️ Requires credentials.json
- ⚠️ Will send to real email addresses

**Browser MCP will:**
- ✅ Actually navigate to websites
- ✅ Actually fill forms
- ⚠️ Could make real payments if approved

**WhatsApp MCP will:**
- ✅ Actually send WhatsApp messages
- ⚠️ Requires WhatsApp Web login

---

## 📊 Testing After Disabling

### Step 1: Verify .env Changed
```bash
cat .env | grep DRY_RUN
# Should show: DRY_RUN=false
```

### Step 2: Test with Small Action
```bash
# Send test email to yourself
python src/mcp/email_mcp.py
```

### Step 3: Check Logs
```bash
# Look for real actions (no [DRY RUN] prefix)
cat vault/Logs/*.log
```

---

## 🎬 Current Setup (Perfect for Demo)

Your current .env file:
```bash
DRY_RUN=true                    # ✅ Safe mode enabled
GMAIL_CLIENT_ID=test_client_id  # ⚠️ Placeholder (not real)
GMAIL_CLIENT_SECRET=test_...    # ⚠️ Placeholder (not real)
```

**This is PERFECT for:**
- ✅ Hackathon demo
- ✅ Testing
- ✅ Showing judges
- ✅ Safe development

---

## ✅ Summary

### Current State:
- DRY_RUN=true (line 15 in .env)
- Safe mode enabled
- No real actions taken
- Perfect for demo

### To Disable:
1. Edit .env file
2. Change `DRY_RUN=true` to `DRY_RUN=false`
3. Setup all credentials first
4. Test carefully

### Recommendation:
**KEEP IT ENABLED for hackathon submission!**

---

*Generated: 2026-03-25 16:32 UTC*
*Current Setting: DRY_RUN=true (SAFE)*
