from django.db import models


class Profession(models.Model):
    objects = models.Manager()
    idProfession = models.IntegerField(db_column="idProfession", primary_key=True)
    professionName = models.TextField(db_column="professionName")

    def __int__(self):
        return self.idProfession

    def __str__(self):
        return self.professionName

    class Meta:
        db_table = 'tblprofession'


class GenLaborFuncContainsProf(models.Model):
    objects = models.Manager()
    idContainsProf = models.IntegerField(primary_key=True, db_column="idContainsProf")
    idGenLaborFunc = models.IntegerField(db_column="idGenLaborFunc")
    idProfession = models.IntegerField(db_column="idProfession")

    class Meta:
        db_table = 'tblgenfunccontainsprof'


class GenFuncContainsFunc(models.Model):
    objects = models.Manager()
    idContainsFunc = models.IntegerField(primary_key=True, db_column="idContainsFunc")
    idGenLaborFunc = models.IntegerField(db_column="idGenLaborFunc")
    idLaborFunc = models.IntegerField(db_column="idLaborFunc")

    class Meta:
        db_table = 'tblgenfunccontainsfunc'


class LaborFuncContainsKnowledge(models.Model):
    objects = models.Manager()
    idContainsKnowledge = models.IntegerField(primary_key=True, db_column="idContainsKnowledge")
    idLaborFunc = models.IntegerField(db_column="idLaborFunc")
    idNecKnowledge = models.IntegerField(db_column="idNecKnowledge")

    class Meta:
        db_table = 'tbllaborfunccontainsknowledge'


class LaborFuncContainsSkill(models.Model):
    objects = models.Manager()
    idContainsSkill = models.IntegerField(primary_key=True, db_column="idContainsSkill")
    idLaborFunc = models.IntegerField(db_column="idLaborFunc")
    idNecSkill = models.IntegerField(db_column="idNecSkill")

    class Meta:
        db_table = 'tbllaborfunccontainsskill'


class NecessaryKnowledge(models.Model):
    objects = models.Manager()
    idNecKnowledge = models.IntegerField(primary_key=True, db_column="idNecKnowledge")
    necKnowledgeName = models.TextField(db_column="necKnowledgeName")
    embeddingKnowledge = models.TextField(db_column="embeddingKnowledge")

    def __str__(self):
        return self.necKnowledgeName

    def __int__(self):
        return self.idNecKnowledge

    class Meta:
        db_table = 'tblnecessaryknowledge'


class NecessarySkill(models.Model):
    objects = models.Manager()
    idNecSkill = models.IntegerField(primary_key=True, db_column="idNecSkill")
    necSkillName = models.TextField(db_column="necSkillName")
    embeddingSkill = models.TextField(db_column="embeddingSkill")

    def __str__(self):
        return self.necSkillName

    def __int__(self):
        return self.idNecSkill

    class Meta:
        db_table = 'tblnecessaryskill'

