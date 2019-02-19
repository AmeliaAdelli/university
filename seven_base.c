/*
На стандартном потоке ввода задается последовательность 
неотрицательных целых и дробных чисел в семеричной системе счисления.
Числа разделяются произвольным количеством пробельных символов. 
Целая часть числа отделяется от дробной знаком . (точка).

На стандартный поток вывода напечатайте числа в обычном виде 
с плавающей точкой в десятичной системе счисления.
*/
#include <ctype.h>
#include <stdio.h>
#include <stdbool.h>

#define BASE 7

int main() {
    bool after_point = false;
    bool number_was_printed = true;

    int symbol;
    double number = 0;

    double current_degree = BASE;

    while ((symbol = getchar()) != EOF) {
        if (isspace(symbol)) {
            if (!number_was_printed) {
                printf("%.10g\n", number);
                number = 0;
                number_was_printed = true;
                after_point = false;
            }
        }

        else {
            number_was_printed = false;
            if (isdigit(symbol)) {
                if (after_point) {
                    number += (symbol - '0') * (1 / current_degree);
                    current_degree *= BASE;
                }
                else {
                    number = number * BASE + (symbol - '0');
                }
            }
            else {
                if (symbol == '.') {
                    after_point = true;
                    current_degree = BASE;
                }
            }
        }
    }

    if (!number_was_printed) {
        printf("%.10g\n", number);
    }
    return 0;
}
