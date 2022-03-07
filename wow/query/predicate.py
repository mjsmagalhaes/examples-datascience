from typing import Any, Union, List, Tuple, Callable

FilterPredicate = Callable[[Any], bool]

MapFunction = Callable[[Any], Any]
MapPredicate = Union[MapFunction, List[MapFunction], Tuple[MapFunction]]


class Predicate:
    """
    A factory of predicates used in Query.
    """

    # === FILTER Predicates ===

    @staticmethod
    def any(fns):
        return lambda x: any(map(lambda f: f(x), fns))

    @staticmethod
    def all(fns):
        return lambda x: all(map(lambda f: f(x), fns))

    @staticmethod
    def isActionCompound() -> FilterPredicate:
        return lambda r: type(r['action_e1']) == list

    # --- FILTER Predicates: Target ---

    @staticmethod
    def isTarget(target) -> FilterPredicate:
        return lambda x: x.target == target

    @staticmethod
    def isTargetHostile() -> FilterPredicate:
        return lambda x: x.target_mask.hostile == True

    # --- FILTER Predicates: Actor ---

    @staticmethod
    def isActor(actor) -> FilterPredicate:
        return lambda x: x.actor == actor

    @staticmethod
    def isActorHostile() -> FilterPredicate:
        return lambda x: x.actor_mask.hostile == True

    # --- FILTER Predicates: Actions ---

    @staticmethod
    def isAction(action) -> FilterPredicate:
        return lambda x: x.action == action

    @staticmethod
    def isActionId(id: int) -> FilterPredicate:
        return lambda x: x.action_id == id

    @staticmethod
    def isPlayerAction() -> FilterPredicate:
        return lambda x: x.actor_tag == 'Player' and x.actor != '0'

    def isPetAction() -> FilterPredicate:
        return lambda x: x.actor_tag == 'Pet' and x.actor != '0'

    @staticmethod
    def isCreatureAction() -> FilterPredicate:
        return lambda x: x.actor_tag == 'Creature'

    # --- FILTER Predicates: Events ---
    @staticmethod
    def isEventIn(event_list: List[str]) -> FilterPredicate:
        return lambda x: x.event in event_list

    @classmethod
    def isEncounterStart(cls) -> FilterPredicate:
        return cls.isEventIn(['ENCOUNTER_START'])

    @classmethod
    def isEncounterEnd(cls) -> FilterPredicate:
        return cls.isEventIn(['ENCOUNTER_END'])

    # === MAP Predicates ===

    @staticmethod
    def getData() -> MapPredicate:
        return lambda x: x.data

    @staticmethod
    def getDataIndex(idx) -> MapPredicate:
        return lambda x: x.data[idx]

    @staticmethod
    def getRawData() -> MapPredicate:
        return lambda x: x.rawdata

    @staticmethod
    def getEvent() -> MapPredicate:
        return lambda x: x.event

    @staticmethod
    def getTimestamp() -> MapPredicate:
        return lambda x: x.getTimestamp()

    @staticmethod
    def getTimestampString() -> MapPredicate:
        return lambda x: x.getTimestampString()

    # --- MAP Predicates: Actor ---

    @staticmethod
    def getActor() -> MapPredicate:
        return lambda x: x.actor

    @staticmethod
    def getActorTag() -> MapPredicate:
        return lambda x: x.actor_tag

    @staticmethod
    def getActorId() -> MapPredicate:
        return lambda x: x.actor_id

    @staticmethod
    def getActorFlags() -> MapPredicate:
        return lambda x: x.actor_flags

    @classmethod
    def getActorInfo(cls) -> MapPredicate:
        return (
            cls.getActor(),
            cls.getActorTag(),
            cls.getActorId()
        )

    # --- MAP Predicates: Target ---

    @staticmethod
    def getTarget() -> MapPredicate:
        return lambda x: x.target

    @staticmethod
    def getTargetTag() -> MapPredicate:
        return lambda x: x.target_tag

    @staticmethod
    def getTargetId() -> MapPredicate:
        return lambda x: x.target_id

    @staticmethod
    def getTargetFlags() -> MapPredicate:
        return lambda x: x.target_flags

    @classmethod
    def getTargetInfo(cls) -> MapPredicate:
        return (
            cls.getTarget(),
            cls.getTargetTag(),
            cls.getTargetId()
        )

    # --- MAP Predicates: Actions ---

    @staticmethod
    def getAction() -> MapPredicate:
        return lambda x: x.action

    @staticmethod
    def getActionId() -> MapPredicate:
        return lambda x: x.action_id
