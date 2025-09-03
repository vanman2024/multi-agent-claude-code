#!/bin/bash

# Display the idea management menu
echo "What would you like to do with ideas?"
echo ""
echo "1. 💡 Create new discussion"
echo "2. 📋 List existing discussions"
echo "3. 🔄 Convert discussion to issue"
echo "4. 👁️ View specific discussion"
echo ""
echo -n "Choose [1-4]: "
read CHOICE

case "$CHOICE" in
  1) ./scripts/idea/create.sh ;;
  2) ./scripts/idea/list.sh ;;
  3) ./scripts/idea/convert.sh ;;
  4) ./scripts/idea/view.sh ;;
  *) echo "Invalid choice"; exit 1 ;;
esac