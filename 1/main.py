from calculator import Calculator


def main():
    calc = Calculator()

    operations = {
        "1": calc.add,
        "2": calc.subtract,
        "3": calc.multiply,
        "4": calc.divide
    }

    while True:
        print("\n===== Advanced Calculator =====")
        print("1. Add")
        print("2. Subtract")
        print("3. Multiply")
        print("4. Divide")
        print("5. Show History")
        print("6. Clear History")
        print("7. Show Operations Used")
        print("8. Use Last Result")
        print("9. Exit")

        choice = input("Choose an option (1-9): ").strip()

        if choice == "9":
            print("Exiting calculator. Goodbye!")
            break

        elif choice in operations:
            try:
                num1 = float(input("Enter first number: "))
                num2 = float(input("Enter second number: "))
                result = operations[choice](num1, num2)
                print(f"Result: {result:.2f}")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "5":
            history = calc.get_history()
            if not history:
                print("No history available.")
            else:
                print("\n---- Calculation History ----")
                for op, a, b, result in history:
                    print(f"{a} {op} {b} = {result:.2f}")

        elif choice == "6":
            calc.clear_history()
            print("History cleared.")

        elif choice == "7":
            ops = calc.get_operations_used()
            print("Operations used:", ", ".join(ops) if ops else "None")

        elif choice == "8":
            last_result = calc.get_last_result()
            if last_result is None:
                print("No previous result available.")
                continue

            print(f"Using last result: {last_result}")

            try:
                num2 = float(input("Enter second number: "))
                op_choice = input("Choose operation (1:Add, 2:Sub, 3:Mul, 4:Div): ").strip()

                if op_choice in operations:
                    result = operations[op_choice](last_result, num2)
                    print(f"Result: {result:.2f}")
                else:
                    print("Invalid operation choice.")

            except ValueError as e:
                print(f"Error: {e}")

        else:
            print("Invalid choice. Please select a valid option.")


if __name__ == "__main__":
    main()