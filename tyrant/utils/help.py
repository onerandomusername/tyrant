from discord import Embed
from discord.ext import commands
from discord.ext.commands import Bot

from tyrant import constants


class TyrantHelp(commands.HelpCommand):
    """Help command for tyrant."""

    def fmt_command_aliases(self, command: commands.Command, add_parenthesis:bool=False):
        """Return a formatted string displaying all the aliases of a command."""
        aliases_str = " | ".join(list(command.aliases))

        return f"({aliases_str})" if add_parenthesis else aliases_str

    async def send_bot_help(self, mapping):
        """Tyrant's help menu command."""
        bot = self.context.bot
        help_embed = Embed(
            title="Help",
            description="Tyrant help list.",
            color=constants.Color.yellow,
        )
 
        for cog_name in bot.cogs:
            cog = bot.cogs[cog_name]
            field_value = ""

            for cmd in await self.filter_commands(cog.get_commands(), sort=True):
                if isinstance(cmd, commands.Group):
                    for sub_cmd in await self.filter_commands(cmd.commands, sort=True):
                        field_value += f"**{constants.Bot.prefix}{cmd.name} {sub_cmd.name}** [{' | '.join(list(sub_cmd.aliases))}]\n"
                else:
                    field_value += f"**{constants.Bot.prefix}{cmd.name}** [{' | '.join(list(cmd.aliases))}]\n"

            if field_value != "":
                help_embed.add_field(name=cog_name, value=field_value, inline=False)

        await self.get_destination().send(embed=help_embed)

    async def send_command_help(self, command: commands.Command):
        """Post help for specified command."""
        help_embed = Embed(
            title=f"{constants.Bot.prefix}{command.name} [{' | '.join(list(command.aliases))}]",
            description=(
                command.help if command.description == "" else command.description
            ),
            color=constants.Color.yellow,
        )

        await self.get_destination().send(embed=help_embed)

    async def send_group_help(self, group:commands.Group):
        """Post help for command groups."""
        subcommands = group.commands
        if len(subcommands) == 0:
            await self.send_command_help(group)
            return

        commands_ = await self.filter_commands(subcommands, sort=True)
        help_embed = Embed(
            title=f"**{group.name}** Help",
            color=constants.Color.yellow
        )
        message = ""

        for command in commands_:
            message += f"**{constants.Bot.prefix}{group.name} {command.name}** [{' | '.join(list(command.aliases))}]\n"

        help_embed.description = message 
        await self.get_destination().send(embed=help_embed)

    async def send_error_message(self, error):
        """Post error message when an error occurs."""
        help_embed: Embed = Embed(
            title="Oops!", description=error, color=constants.Color.yellow
        )

        await self.get_destination().send(embed=help_embed)
