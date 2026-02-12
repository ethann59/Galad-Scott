import esper
from src.components.special.speScoutComponent import SpeScout
from src.components.special.speLeviathanComponent import SpeLeviathan
from src.components.special.speKamikazeComponent import SpeKamikazeComponent
from src.components.special.isVinedComponent import isVinedComponent
from src.components.core.radiusComponent import RadiusComponent

class CapacitiesSpecialesProcessor(esper.Processor):
    def process(self, dt, **kwargs):
        # Scout : manœuvre d'évasion (invincibilité)
        for ent, speScout in esper.get_component(SpeScout):
            speScout.update(dt)
        
        # Leviathan : seconde salve (instantané, cooldown)
        for ent, speLeviathan in esper.get_component(SpeLeviathan):
            speLeviathan.update(dt)

        # Kamikaze : boost de vitesse
        for ent, speKamikaze in esper.get_component(SpeKamikazeComponent):
            speKamikaze.update(dt)

        # Gérer le cooldown de base (soin/attaque) pour all units
        # qui n'ont pas déjà été affectées par l'Architecte ce tick.
        for ent, radius in esper.get_component(RadiusComponent):

            if radius.cooldown > 0:
                old_cooldown = radius.cooldown
                radius.cooldown -= dt  # Utiliser dt, c'est plus précis
                if radius.cooldown < 0:
                    radius.cooldown = 0
                # Log for Leviathan only (entity with SpeLeviathan component)
                if esper.has_component(ent, SpeLeviathan) and int(old_cooldown) != int(radius.cooldown):
                    print(f"[DEBUG] CapacitiesSpecialesProcessor - Entity {ent} radius.cooldown: {old_cooldown:.1f} -> {radius.cooldown:.1f} (dt={dt:.3f})")