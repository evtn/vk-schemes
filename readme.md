# VK Schemes

Набор цветовых схем для vk.com.    
Для покраски используются переменные с сайта (дополнительные стили применяются только к логотипу).    
На момент написания этого текста, многие элементы не были прокрашены, поэтому схемы могут выглядеть незаконченными (особенно темные).    

## Установка

1. Установить менеджер стилей с поддержкой UserCSS (желательно, [Stylus](https://github.com/openstyles/stylus/)):
    - [Firefox](https://addons.mozilla.org/firefox/addon/styl-us/)
    - [Opera](https://addons.opera.com/extensions/details/stylus/)
    - [Chrome/Chromium/Яндекс/etc](https://chrome.google.com/webstore/detail/stylus/clngdbkpkpeebahjckkjfobafhncgmne)

2. Выбрать схему (скриншоты ниже) и перейти по соответствующей ссылке:
    - [vk.com Light](https://github.com/evtn/vk-schemes/raw/build-stable/vk-default-scheme.user.css)
    - [vk.com Dark](https://github.com/evtn/vk-schemes/raw/build-stable/vk-dark-scheme.user.css)
    - [Ocean](https://github.com/evtn/vk-schemes/raw/build-stable/vk-ocean-scheme.user.css)
    - [Acid Dark](https://github.com/evtn/vk-schemes/raw/build-stable/vk-acid_dark-scheme.user.css)
    - [Leaf](https://github.com/evtn/vk-schemes/raw/build-stable/vk-leaf-scheme.user.css)

## Добавление своих схем

Чтобы добавить свою схему:    
(Шаги 3-4 нужно выполнять из корня репозитория)    

1. Скопируйте репозиторий.    
2. Добавьте схему в `build/schemes.json` (подробнее о структуре схем в [`build/readme.md`](build/readme.md))    
3. Запустите `build/optimizer.py` для очистки лишних переменных.    
4. Запустите `build/builder.py` для сборки схем.    
5. Скопируйте содержимое вашей собранной схемы из соотсветствующего файла в папке `styles` и проверьте ее работоспособность.    
6. Удалите собранные схемы и делайте PR.    