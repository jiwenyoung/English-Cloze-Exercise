#!/bin/bash

#Python Part
rm -rf ./dist
pyinstaller --clean -D cloze.py
cp -a ./config ./dist/cloze/config
cp -a ./log ./dist/cloze/log
cp -a ./data ./dist/cloze/data
cp -a ./articles ./dist/cloze/articles
rm -rf ./build
rm -rf ./cloze.spec

#Eelecton Part
#cd ..
#./node_modules/.bin/electron-packager . --overwrite --ignore=cli$ --out=release
#cp -a ./cli/dist/cloze ./release/english-cloze-linux-x64/resources/app/cloze
