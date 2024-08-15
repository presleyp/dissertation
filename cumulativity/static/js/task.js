$(document).ready(function(){
    var mySperiment = cumulativity_experiment7;
    var psiturk = PsiTurk(uniqueId, adServerLoc);
    psiturk.finishInstructions();
    var speriment = new Experiment(mySperiment, condition, counterbalance, psiturk);
    speriment.start();
});