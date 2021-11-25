  Random rnd = new Random();
  int n = rnd.Next(0,10);
  Console.WriteLine("Введите число");
  int player = Convert.ToInt32(Console.ReadLine());
  if (player == n) {
    Console.WriteLine("Вы - угадали");
  } else{
        Console.WriteLine("Вы - не угадали, правильный ответ: "+n);
  }
