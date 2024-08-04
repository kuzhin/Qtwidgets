# Qtwidgets



Для решения  использовались python3 + pyqt5 + h5py + numpy + scipy + pyqtgraph.
Код, работающий с numpy был векторизован, без циклов для подсчета суммы.

Необходимо было сделать:
Окно с таблицей и графиком.
1.  Окно должно содержать таблицу с числами и график под таблицей.
2.  Все данные внутри должны храниться в двумерном numpy-массиве.
3.  Один из столбцов должен позволять редактировать числа только из выпадающего списка чисел от 1 до 5.
4.  Значения в одном из столбцов должны пересчитываться из значений в этой же строчке в другом столбце.
5.  Значения в одном из столбцов должны содержать накопленную сумму значений из другого столбца.
6.  В одном из столбцов ячейки должны заливаться красным или зеленым цветом в зависимости от того, положительные они или отрицательные.
7.  При выборе двух столбцов должен отображаться график зависимости Второго выбранного столбца от Первого.
8.  Нужны кнопки для сохранения массива в текстовый файл или в hdf, загрузки его из текстового файла или hdf, для изменения размера массива и заполнения его (кроме особенных ячеек, которые пересчитываются) случайными значениями.
