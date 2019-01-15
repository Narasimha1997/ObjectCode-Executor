
int main(int argc, char const *argv[]){

    struct node {
        int id;
        char *stack;
    };

    struct node Node = {10, "Hello, world"};

    int c = Node.id;

    return c;  
}
