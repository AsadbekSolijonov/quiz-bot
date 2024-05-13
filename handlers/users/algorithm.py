from utils.db_api.db import QuestionCategory, Question, Answer

questions = Question()


class Queue:
    def __init__(self, category_id):
        self.items = questions.objects_all(cat_id=category_id)

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if not self.isEmpty():
            return self.items.pop(0)
        else:
            print("Queue is empty")

    def peek(self):
        if not self.isEmpty():
            return self.items[0]
        else:
            print("Queue is empty")

    def size(self):
        return len(self.items)


# Example usage:
# queue = Queue()
# queue.enqueue(1)
# queue.enqueue(2)
# queue.enqueue(3)
# print("Queue:", queue.items)
# print("Peek:", queue.peek())
# print("Dequeue:", queue.dequeue())
# print("Queue after dequeuing:", queue.items)
