class TeamUtil:
    # utility function to return list of users in a team -> works for both team and individual event
    def get_participants_json_from_team(self, t):
        participants = []
        for u in list(t.user.all()):
            participant = {
                "user_id": u.user.id,
                "first_name": u.user.first_name,
                "last_name": u.user.last_name,
                "email": u.user.email,
            }
            try:
                for d in list(u.user.details.all()):
                    participant["college"] = d.college
                    participant["mobile"] = d.mobile
                    break
            except:
                pass

            participants.append(participant)

        return participants
