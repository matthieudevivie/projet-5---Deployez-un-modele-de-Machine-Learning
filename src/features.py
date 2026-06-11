from sklearn.base import BaseEstimator, TransformerMixin

class FeatureEngineer(BaseEstimator, TransformerMixin):
    
    def __init__(self):
        pass
    
    def fit(self, X, y=None): 
        self.mediane_par_poste_ = (
            X.groupby('poste')['revenu_mensuel'].median()
        )
        self.mediane_par_education_ = (
            X.groupby('niveau_education')['revenu_mensuel'].median()
        )
        return self
    
    def transform(self, X):
        X = X.copy()
        
        X['jeune'] = (X['age'] < 33).astype(int)
        X['bas_revenu'] = (X['revenu_mensuel'] < 3000).astype(int)
        X['premiere_annee'] = (X['annees_dans_l_entreprise'] < 1).astype(int)
        X['sans_pee'] = (X['nombre_participation_pee'] == 0).astype(int)
        X['jeune_et_premiere_annee'] = (
            (X['age'] < 33) & (X['annees_dans_l_entreprise'] < 1)
        ).astype(int)
        
        X['satisfaction_globale'] = (
            X['satisfaction_employee_environnement']
            + X['satisfaction_employee_nature_travail']
            + X['satisfaction_employee_equipe']
            + X['satisfaction_employee_equilibre_pro_perso']
        ) / 4
        
        X['ratio_stagnation'] = (
            X['annees_depuis_la_derniere_promotion']
            / (X['annees_dans_l_entreprise'] + 0.1)
        )
        
        X['ratio_salaire_mediane_poste'] = (
            X['revenu_mensuel'] / X['poste'].map(self.mediane_par_poste_)
        )
        X['ratio_salaire_mediane_education'] = (
            X['revenu_mensuel'] / X['niveau_education'].map(self.mediane_par_education_)
        )
        
        return X