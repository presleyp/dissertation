$(document).ready(function(){
    var mySperiment = alternations_experiment_june;
    var psiturk = PsiTurk(uniqueId, adServerLoc);
    psiturk.finishInstructions();
    var speriment = new Experiment(mySperiment, condition, counterbalance, psiturk);
    speriment.start();
});