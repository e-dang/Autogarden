
from typing import Any
from django.db.models import Model


class ModelFormatter:
    def __init__(self, instance: Model) -> None:
        self.instance = instance

    def __getattribute__(self, name: str) -> Any:
        try:
            return super().__getattribute__(name)
        except AttributeError:
            format_attr = f'get_{name}_display'
            try:
                return super().__getattribute__(format_attr)()
            except AttributeError:
                return getattr(super().__getattribute__('instance'), name)


class GardenFormatter(ModelFormatter):
    CONNECTED_STR = 'Connected'
    DISCONNECTED_STR = 'Disconnected'
    CONNECTED_BADGE = 'badge-success'
    DISCONNECTED_BADGE = 'badge-danger'

    # Values from https://www.speedcheck.org/wiki/rssi/#:~:text=RSSI%20or%20this%20signal%20value,%2D70%20(minus%2070).
    CONN_POOR = -80
    CONN_OK = -70
    CONN_GOOD = -67
    CONN_EXCELLENT = -30

    CONN_NOT_AVAILABLE_MSG = 'N/A'
    CONN_BAD_MSG = 'Bad'
    CONN_POOR_MSG = 'Poor'
    CONN_OK_MSG = 'Ok'
    CONN_GOOD_MSG = 'Good'
    CONN_EXCELLENT_MSG = 'Excellent'

    CONN_NOT_AVAILABLE_BADGE = 'badge-danger'
    CONN_BAD_BADGE = 'badge-danger'
    CONN_POOR_BADGE = 'badge-warning'
    CONN_OK_BADGE = 'badge-warning'
    CONN_GOOD_BADGE = 'badge-success'
    CONN_EXCELLENT_BADGE = 'badge-success'

    WL_OK_BADGE = 'badge-success'
    WL_LOW_BADGE = 'badge-danger'

    def get_is_connected_display(self) -> str:
        return self.CONNECTED_STR if self.instance.is_connected else self.DISCONNECTED_STR

    def get_is_connected_badge_class(self) -> str:
        return self.CONNECTED_BADGE if self.instance.is_connected else self.DISCONNECTED_BADGE

    def get_is_connected_element(self) -> str:
        return self._create_badge(
            'connectionStatus',
            self.get_is_connected_badge_class(),
            self.get_is_connected_display()
        )

    def get_connection_strength_display(self) -> str:
        if self.instance.connection_strength is None:
            return self.CONN_NOT_AVAILABLE_MSG
        elif self.instance.connection_strength >= self.CONN_EXCELLENT:
            return self.CONN_EXCELLENT_MSG
        elif self.instance.connection_strength >= self.CONN_GOOD:
            return self.CONN_GOOD_MSG
        elif self.instance.connection_strength >= self.CONN_OK:
            return self.CONN_OK_MSG
        elif self.instance.connection_strength >= self.CONN_POOR:
            return self.CONN_POOR_MSG
        else:
            return self.CONN_BAD_MSG

    def get_connection_strength_badge_class(self) -> str:
        if self.instance.connection_strength is None:
            return self.CONN_NOT_AVAILABLE_BADGE
        elif self.instance.connection_strength >= self.CONN_EXCELLENT:
            return self.CONN_EXCELLENT_BADGE
        elif self.instance.connection_strength >= self.CONN_GOOD:
            return self.CONN_GOOD_BADGE
        elif self.instance.connection_strength >= self.CONN_OK:
            return self.CONN_OK_BADGE
        elif self.instance.connection_strength >= self.CONN_POOR:
            return self.CONN_POOR_BADGE
        else:
            return self.CONN_BAD_BADGE

    def get_connection_strength_element(self) -> str:
        return self._create_badge(
            'connectionStrength',
            self.get_connection_strength_badge_class(),
            self.get_connection_strength_display()
        )

    def get_water_level_badge_class(self):
        return self.WL_LOW_BADGE if self.instance.water_level == self.instance.LOW else self.WL_OK_BADGE

    def get_water_level_element(self):
        return self._create_badge(
            'waterLevel',
            self.get_water_level_badge_class(),
            self.instance.get_water_level_display()
        )

    def get_update_frequency_display(self) -> str:
        total = self.instance.update_frequency.total_seconds()
        minutes, seconds = divmod(total, 60)
        minutes = int(minutes)
        seconds = int(seconds)
        string = ''
        if minutes != 0:
            string += f'{minutes} Min '
        if seconds != 0:
            string += f'{seconds} Sec'
        return string.strip()

    def get_last_connection_time_display(self) -> str:
        if self.instance.last_connection_time is None:
            return str(None)
        return self.instance.last_connection_time.strftime('%-m/%d/%Y %I:%M %p')

    def _create_badge(self, id_: str, klass: str, text: str) -> str:
        return f'''
                <span class="lead">
                    <span id="{id_}" class="badge badge-pill {klass}">
                        {text}
                    </span>
                </span>
        '''
