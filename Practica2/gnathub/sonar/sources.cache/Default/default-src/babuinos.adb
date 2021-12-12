-- AUTOR@S: LAURA CAVERO y AISHA GANDAROVA

With Ada.Text_IO; Use Ada.Text_IO;
With def_semafors; Use def_semafors;
With ada.Numerics.Discrete_Random;

procedure Babuinos is
   type randRange is range 1..100;
   package Rand_Int is new ada.numerics.discrete_random(randRange);
   use Rand_Int;
   gen : Generator;
   num : randRange;

   semContNord: Semafor(3);
   semContSud: Semafor(3);
   semBabuiNord: Semafor(1);
   semBabuiSud: Semafor(1);
   semCordaBuit: Semafor(1);

   task type BabuinoNord;
   task type BabuinoSud;

   task body BabuinoNord is
      contadorN: Natural := 0;
   begin
      for i in 1..5 loop
         reset(gen);
         num:= Random(gen);

         -- Llegan a la cuerda para cruzarla (espera)
         Put_Line("BON DIA, soc en Babuí Nord" & Integer'Image(i)
               & " i vaig cap al Sud");

         semBabuiNord.Wait;
         if contadorN = 0 then
            semCordaBuit.Wait; -- Bloqueamos Babuinos de la otra dirección
            contadorN := contadorN + 1;
         end if;
         semBabuiNord.Signal;

         semContNord.Wait; -- El Babuino está atravesando la cuerda
         Put_Line("*****A la corda n'hi ha"
               & Integer'Image(contadorN) & " direcció Sud*****");

         Put_Line("Nord" & Integer'Image(i) &
                 ": És a la corda i travessa cap al Sud");
         delay 0.5; -- **Cruzando la cuerda**
         semContNord.Signal;

         semBabuiNord.Wait;
         contadorN := contadorN - 1;
         Put_Line("Nord" & Integer'Image(i) & " ha arribat a la vorera");

         if contadorN = 0 then
            semCordaBuit.Signal;
         end if;
         semBabuiNord.Signal;

      end loop;
   end BabuinoNord;

   task body BabuinoSud is
      contadorS: Natural := 0;
   begin
      for i in 1..5 loop
         reset(gen);
         num:= Random(gen);

         -- Llegan a la cuerda para cruzarla (espera)
         Put_Line("     BON DIA, soc en Babuí Sud" & Integer'Image(i)
               & " i vaig cap al Nord");

         semBabuiSud.Wait;
         if contadorS = 0 then
            semCordaBuit.Wait; -- Bloqueamos Babuinos de la otra dirección
            contadorS := contadorS + 1;
         end if;
         semBabuiSud.Signal;

         semContSud.Wait; -- El Babuino está atravesando la cuerda
         Put_Line("     +++++A la corda n'hi ha"
               & Integer'Image(contadorS) & " direcció Nord+++++");

         Put_Line("     Sud" & Integer'Image(i) &
                 ": És a la corda i travessa cap al Nord");
         delay 0.5; -- **Cruzando la cuerda**
         semContSud.Signal;

         semBabuiSud.Wait;
         contadorS := contadorS - 1;
         Put_Line("     Sud" & Integer'Image(i) & " ha arribat a la vorera");

         if contadorS = 0 then
            semCordaBuit.Signal;
         end if;
         semBabuiSud.Signal;

      end loop;
   end BabuinoSud;

begin
   declare
      p : BabuinoNord;
      q : BabuinoSud;
   begin
      null;
   end;

end Babuinos;
