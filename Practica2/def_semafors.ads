-- AUTOR@S: LAURA CAVERO y AISHA GANDAROVA

package def_semafors is
   protected type Semafor (Inicial: Natural) is
      entry Wait;
      procedure Signal;
   private
      Contador: Natural := Inicial;
   end Semafor;
end def_semafors;
