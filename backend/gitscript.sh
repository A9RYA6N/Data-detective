#!/usr/bin/env bash
DATE_DATA=""

getcurrenttime(){
    DATE_DATA=$(date "+%Y-%m-%d %I:%M %p")
}

echo "Enter commit message"
read COMMIT_MESSAGE

echo "Do you want to commit? y/n"
read CONFIRM_COMMIT

case ${CONFIRM_COMMIT,,} in
    n|no)
        echo "Abort. Nothing committed."
        exit 0
        ;;
    y|yes)
        ;;
    *)
        echo "Error: Invalid input. Exiting."
        exit 1
        ;;
esac

echo "Do you want to push to repo? y/n"
read CONFIRM_PUSH

git add .
git commit -m "$COMMIT_MESSAGE"

case ${CONFIRM_PUSH,,} in
    y|yes)
        echo "Pushing to repo..."
        git push
        ;;
    n|no)
        echo "Commited locally and logged"
        ;;
    *)
        echo "Error: Invalid input. Exiting without logging."
        exit 1
esac

getcurrenttime

if [ ${CONFIRM_PUSH,,} = y ] || [ ${CONFIRM_PUSH,,} = yes ]; then
    echo "Committed and pushed on $DATE_DATA with message: '$COMMIT_MESSAGE'" >> gitlogs.txt
else
    echo "Committed on $DATE_DATA with message: '$COMMIT_MESSAGE'" >> gitlogs.txt
fi
