#!/bin/bash
set -e

app(){
  python ./app.py 
}
bot(){
  python ./bot.py 
}


case "$1" in
  app)
    shift
    app
    ;;
  bot)
    shift
    bot
    ;;
  *)
    exec "$@"
    ;;
esac