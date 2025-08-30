import discord
from discord.ext import commands
import asyncio
import json
import os
from datetime import datetime
from config import TOKEN

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='+', intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f'{bot.user} connecté et prêt!')
    try:
        synced = await bot.tree.sync()
        print(f"Synchronisé {len(synced)} commande(s)")
    except Exception as e:
        print(f"Erreur de synchronisation: {e}")

@bot.tree.command(name="dmall", description="Envoie un message privé à tous les membres du serveur")
async def dmall(interaction: discord.Interaction, message: str):
    if not interaction.user.guild_permissions.administrator:
        embed = discord.Embed(
            title="",
            description="Vous devez être administrateur pour utiliser cette commande.",
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    guild = interaction.guild
    members = [member for member in guild.members if not member.bot and not member.status == discord.Status.offline]
    
    if not members:
        embed = discord.Embed(
            title="",
            description="Personne est sur ton serveur",
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    embed = discord.Embed(
        title="",
        description=f"Envoi du message à **{len(members)}** membres...",
    )
    embed.add_field(name="Message", value=message, inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)

    success_count = 0
    failed_count = 0
    failed_members = []

    for member in members:
        try:
            await member.send(message)
            success_count += 1
            
            if success_count % 10 == 0:
                progress_embed = discord.Embed(
                    description=f"`✅` **{success_count}** messages envoyés\n`❌` **{failed_count}** échecs",
                )
                await interaction.edit_original_response(embed=progress_embed)
            
            await asyncio.sleep(0.1)
            
        except discord.Forbidden:
            failed_count += 1
            failed_members.append(member.name)
        except Exception as e:
            failed_count += 1
            failed_members.append(f"{member.name} (Erreur: {str(e)})")

    final_embed = discord.Embed(
        title="",
        description=f"**{success_count}** messages envoyés avec succès\n**{failed_count}** échecs",
    )
    
    if failed_members:
        failed_list = "\n".join(failed_members[:10])
        if len(failed_members) > 10:
            failed_list += f"\n... et {len(failed_members) - 10} autres"
        final_embed.add_field(name="Membres en échec", value=failed_list, inline=False)
    
    await interaction.edit_original_response(embed=final_embed)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title="",
            description="Vous n'avez pas les permissions nécessaires pour cette commande",
        )
        await ctx.send(embed=embed)
    elif isinstance(error, commands.CommandNotFound):
        pass
    else:
        embed = discord.Embed(
            title="",
            description=f"Une erreur s'est produite: `{str(error)}`",
        )
        await ctx.send(embed=embed)

if __name__ == "__main__":
    if TOKEN == "your_bot_token_here":
        print("Erreur: Veuillez configurer votre token dans config.py")
        exit(1)
    
    bot.run(TOKEN)
