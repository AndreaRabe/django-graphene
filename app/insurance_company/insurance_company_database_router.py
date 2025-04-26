class InsuranceCompanyRouter:
    """
    Routeur pour l'application 'insurance_company'.
    Redirige toutes les opérations liées à l'application 'insurance_company'
    vers la base de données 'insurance_company_db'.
    """

    def db_for_read(self, model, **hints):
        """
        Suggère la base de données pour les opérations de lecture.
        """
        if model._meta.app_label == 'insurance_company':
            return 'insurance_company_db'
        return None

    def db_for_write(self, model, **hints):
        """
        Suggère la base de données pour les opérations d'écriture.
        """
        if model._meta.app_label == 'insurance_company':
            return 'insurance_company_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Autorise les relations entre les objets de l'application 'insurance_company'.
        """
        if obj1._meta.app_label == 'insurance_company' or obj2._meta.app_label == 'insurance_company':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Assure que les migrations sont appliquées uniquement à la base de données 'insurance_company_db'
        pour l'application 'insurance_company'.
        """
        if app_label == 'insurance_company':
            return db == 'insurance_company_db'
        return None
