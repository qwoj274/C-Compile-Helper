#include <iostream>
#include <vector>
#include <random>
#include <string>

class MyClass {
private:
    int _value;
    int _id;
    inline static std::vector<int> id_list = {};
    inline static std::mt19937 rng{std::random_device{}()};
    inline static std::uniform_int_distribution<int> dist{10000, 99999};

    bool generateUniqueID() {
        int desired_id = dist(rng);

        for (int id : id_list) {
            if (id == desired_id) {
                return false;
            }
        }
        
        id_list.push_back(desired_id);
        this->_id = desired_id;
        return true;
    }

public:
    MyClass(int value) {
        this->_value = value;
        bool generated = false;
        do {
            generated = generateUniqueID();
        } while (!generated);
    }

    int getValue() {
        return this->_value;
    }

    int getID() {
        return this->_id;
    }

    std::string printInfo() {
        std::string info = std::to_string(this->_id) + " : " + std::to_string(this->_value);
        std::cout << info << std::endl;
        return info;
    }

    std::string printValue() {
        std::string value = std::to_string(this->_value) + "\n";
        return value;
    }

    std::string printID() {
        std::string id = std::to_string(this->_id) + "\n";
        return id;
    }
};


int main() {
    std::vector<MyClass> objects = {};
    for (int i = 0; i < 100; i++ ) {
        MyClass* newObj = new MyClass(i);
        objects.push_back(*newObj);
        newObj->printInfo();
        delete(newObj);
    }
    return 0;
}