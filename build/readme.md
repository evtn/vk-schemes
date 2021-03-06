# build

Различные файлы для сборки стилей через GH Actions    

## Файлы

Директория `schemes` содержит информацию о иерархии схем и их переменных.    
Пример структуры можно посмотреть в `build/schemes/ayu.json`    

-   Если вы хотите добавить альтернативный вариант существующей схемы, добавьте его в файл этой схемы    
-   Если вы хотите добавить свою схему, создайте отдельный `.json`-файл под него

`build.py` собирает стили, опираясь на информацию из `schemes.json` (автогенерируемый файл) и вставляет собранные схемы в `ťemplate.css`    

## Структура схемы

Схема - объект в корне файла схемы (файлы находятся в `/build/styles/`). Ключ схемы, естественно, должен быть уникален и должен быть валидным именем файла.    
Ключи, которые должны быть в каждой схеме:    

- `name`: Имя схемы.    
- `description`: Описание схемы.
- `parent` (опционально): Ключ схемы-родителя или массив ключей (множественное наследование).   
- `variables`: Объект с переменными схемы (см. ниже)    
- `variant_for` (опционально): Ключ схемы, для которой данная схема является вариантом. Влияет на отображение в readme
- `skip` (опционально): если `true`, то схема не будет собираться и добавляться в readme. Полезно для шаблонов

### Переменные

Для упрощения создания, схемы опираются друг на друга и наследуют переменные.    
Также, во избежание многочисленных повторений и улучшения читабельности используются две дополнительных конструкции:    
`@name` - использует значение переменной name из этой же схемы (после того, как это значение будет определено)    
`$name` - конвертируется в `var(--name)` для неизвестных переменных, для переменных из стандартной палитры ВК конвертируется в их значение    

Дополнительно доступна конкатенация (пока довольно ограниченная), например:    
`@name:99` - соединяет значение переменной name и "99".    
Пока доступно только в формате `@x:y`, где x - имя переменной (см. выше) и y - произвольный текст.    
