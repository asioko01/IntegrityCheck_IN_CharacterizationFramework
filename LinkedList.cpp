#include <iostream>
#include <cstdlib>
#include <ctime>
#include <unordered_set>
#include <climits>
#include <algorithm>
#include <chrono>
#include <unistd.h>
#include <stdlib.h>
#include <signal.h>

using namespace std;

const long int N = 245000000; // size of the list

static volatile sig_atomic_t s_got=0;

void sig_handler(int signum){
	s_got = 1;

}

struct Node
{
  uint64_t data;
  Node *next;
};



// 64-bit linear-feedback shift register (LFSR) algorithm
uint64_t lfsr_init()
{
  static uint64_t x = 1;
  uint64_t bit = ((x >> 0) ^ (x >> 1) ^ (x >> 3) ^ (x >> 4) ^ (x >> 64)) & 1;
  x = (x << 1) | bit;
  return x; // return a random number between 0 and 2^64-1 (inclusive)
}

bool lfsr_check(Node *head)
{
  Node *current = head;
  bool firstSwap=true;
  uint64_t bit;

  while (current != nullptr)
  {
    static uint64_t x=1;
    bit = ((x >> 0) ^ (x >> 1) ^ (x >> 3) ^ (x >> 4) ^ (x >> 64)) & 1;
    x = (x << 1) | bit;
    if(firstSwap)
      x+=1;   
    if (current->data != x)
      return true;
    firstSwap=false;
    current = current->next;
  }
  return false;
}

// function to print the linked list
void printList(Node *head)
{
  Node *current = head;
  while (current != nullptr)
  {
    cout << current->data << " ";
    current = current->next;
  }
  cout << endl;
}

// function to find the uniqueness of the numbers in the linked list
bool checkUniqueness(Node *head)
{
  unordered_set<uint64_t> set;
  Node *current = head;
  while (current != nullptr)
  {
    if (set.count(current->data) > 1)
    {
      return false;
    }
    set.insert(current->data);
    current = current->next;
  }
  return true;
}

// function to create the linked list
Node *createList()
{
  Node *head = nullptr;
  Node *current = nullptr;
  for (int i = 0; i < N; i++)
  {
    Node *newNode = new Node();
    newNode->data = lfsr_init();
    newNode->next = nullptr;
    if (head == nullptr)
    {
      head = newNode;
      current = newNode;
    }
    else
    {
      current->next = newNode;
      current = newNode;
    }
  }
  return head;
}

int main()
{
  
  cout<<"In integrity check initialization"<<endl;
  // auto start_time = std::chrono::high_resolution_clock::now();
  // create the linked list
  Node *head = createList();
  //printList(head);
  // auto end_time = std::chrono::high_resolution_clock::now();
  // auto elapsed_time_ms = std::chrono::duration_cast<std::chrono::milliseconds>(end_time - start_time);
  // std::cout << "Elapsed time: " << elapsed_time_ms.count() << " ms" << std::endl;
  
  cout << "Initialized Complete" << endl;
	
  signal(SIGUSR1,sig_handler);
  while (s_got < 1)
    pause();

  bool int_check = lfsr_check(head);
  cout<<"Integrity Check Complete";
  if (int_check)
    cout << "FAIL";
 
  // printList(head); // print the linked list
  // cout << "Are all the numbers unique in the linked list? " << checkUniqueness(head) << endl; // print the number of unique numbers in the linked list
   return 0;
}
