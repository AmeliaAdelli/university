/*
По данной последовательности постройте дерево, 
запоминая для каждого элемента его значение 
и количество его повторений в последовательности.

Формат ввода
Вводится последовательность целых чисел, заканчивающаяся нулем. 
Сам ноль в последовательность не входит.
Формат вывода
Выведите на экран содержимое дерева в порядке возрастания, 
по одному элементу на строку. 
В каждой строке выводите значение элемента, затем, через пробел, 
укажите, сколько раз он встречается в исходной последовательности.
*/


#include <algorithm>
#include <iostream>
#include <vector>

class node {
 public:
    node* parent = nullptr;
    node* left = nullptr;
    node* right = nullptr;
    int key = 0;
    int freq = 0;
    ~node() {
        if (left != nullptr) {
            delete left;
        }
        if (right != nullptr) {
            delete right;
        }
    }
};

class tree {
 public:
    node* root = nullptr;
    int height = 0;

    explicit tree(int number) {
        root = new node();
        root->key = number;
        root->freq = 1;
    }

    void insert(int number) {
        node* x = root;
        int counter = 1;
        node* y = nullptr;
        while (x != nullptr) {
            y = x;
            if (number < x->key) {
                x = x->left;
            } else if (number > x->key) {
                x = x->right;
            } else {
                x->freq += 1;
                break;
            }
            ++counter;
        }
        if (x == nullptr) {
            node* r = new node();
            r->parent = y;
            r->key = number;
            r->freq = 1;
            if (number < y->key) {
                y->left = r;
            } else {
                y->right = r;
            }
        }

        if (counter > height) {
            height = counter;
        }
    }

    void print_tree(node* start) {
        if (start->left != nullptr) {
            print_tree(start->left);
        }
        std::cout << start->key << " " << start ->freq << "\n";
        if (start->right != nullptr) {
            print_tree(start->right);
        }
    }

    ~tree() {
        delete root;
    }
};

int main() {
    int number;
    std::cin >> number;
    tree t(number);
    std::cin >> number;
    while (number != 0) {
        t.insert(number);
        std::cin >> number;
    }
    t.print_tree(t.root);
    return 0;
}
